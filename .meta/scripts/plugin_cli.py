#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault-wiki 插件生命周期机械核心（装卸 / 合规 / 依赖 / 注入 / 注册表 / 副本同步）。

定位（见 .meta/protocol/actions.md 执行原则）：确定性的结构操作交给本脚本，
语义判断交给 LLM。脚本只碰四处：插件目录进出、AGENTS.md 注入区标记块、
registry.yaml 插件段、.agents/skills/ 命令副本；protocol / reserved 段与手写区永不动。

用法:
  python .meta/scripts/plugin_cli.py ls          # 清单 + 依赖图（按层分组）
  python .meta/scripts/plugin_cli.py validate    # 合规与依赖检查（只读，错误退出码 1）
  python .meta/scripts/plugin_cli.py audit       # 插件附检（发现式执行各插件 scripts/check.py）
  python .meta/scripts/plugin_cli.py inject      # 重建 AGENTS.md 注入区与 check 检查块（幂等）
  python .meta/scripts/plugin_cli.py registry    # 重建 registry.yaml 插件段（幂等）
  python .meta/scripts/plugin_cli.py deploy      # 同步命令部署副本（幂等）
  python .meta/scripts/plugin_cli.py all         # validate + inject + registry + deploy

manifest 最小 YAML 子集：顶层 `key: value`、`key: []`、块式列表（`  - 项`）、
一层字段字典（`  name: 描述`）；双引号包裹的值去引号；行内注释（` #` 起）剥离。

分层（layer，三值）与依赖方向：
- origin（出身：拥有页面领地）与 field（字段：拥有跨页 frontmatter 字段）是底，零依赖
- derived（派生：拥有派生物与写路径义务）居上，只可依赖 origin/field，同层禁依赖

命令-插件绑定（双向声明，validate 校验一致）：
- 命令 frontmatter 增 owner：插件 id（多个用 [a, b] 列表）或 framework（跨切面，显式无主）
- 插件 manifest 增可选字段 commands：本插件驱动的命令名列表
- error 情形：命令缺 owner、owner 指向未装插件、framework 与其他 owner 并列、
  插件声明不存在的命令、任一侧单边声明（owner 未被 commands 认领，或反之）

插件附检契约（scripts/check.py，可选）：
- 必须定义 check(ctx)，返回 issue 列表：{"level": "error"|"warning"|"info", "message": str}
- ctx.root = 仓库根；ctx.pages = [(wiki 相对路径, frontmatter dict, 正文)]，单次扫描共享
- 只读零副作用：修复动作归命令/人，附检只报告；中文消息，无第三方依赖
"""
import ast
import importlib.util
import os
import re
import shutil
import sys
import types

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLUGINS_DIR = os.path.join(ROOT, ".meta", "plugins")
COMMANDS_DIR = os.path.join(ROOT, ".meta", "command")
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")
AGENTS_MD = os.path.join(ROOT, "AGENTS.md")
REGISTRY = os.path.join(ROOT, ".meta", "protocol", "registry.yaml")

# manifest 八字段（id / version / layer / depends / updated / attachment / fields / inject）+ 可选 commands
REQUIRED_KEYS = ["id", "version", "layer", "depends", "updated", "attachment", "fields", "inject"]
LAYERS = ("origin", "field", "derived")
INJECT_START = "<!-- wiki-inject:start -->"
INJECT_END = "<!-- wiki-inject:end -->"
CHECK_SKILL = os.path.join(COMMANDS_DIR, "check", "SKILL.md")
CHECK_INJECT_START = "<!-- check-inject:start -->"
CHECK_INJECT_END = "<!-- check-inject:end -->"
CHECK_SECTION_RE = re.compile(r"^## Checks\n(.*?)(?=^## |\Z)", re.S | re.M)


def ordered_plugins(plugins):
    """按层（origin → field → derived）再按 id 排序；投影区共用。"""
    return sorted(plugins, key=lambda p: (
        LAYERS.index(plugins[p]["layer"]) if plugins[p].get("layer") in LAYERS else len(LAYERS), p))


def strip_quotes(s):
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def strip_comment(s):
    """剥离行内注释（` #` 起）；完整值含 # 前须加引号。"""
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def parse_manifest(path):
    """解析 manifest 的最小 YAML 子集；失败抛出 ValueError。"""
    data, target = {}, None
    for raw in open(path, encoding="utf-8").read().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if target is None:
                raise ValueError(f"list item before any key: {raw!r}")
            item = strip_quotes(strip_comment(raw.strip()[2:]))
            if not isinstance(data.get(target), list):
                data[target] = []
            data[target].append(item)
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not m:
            raise ValueError(f"unparsable line: {raw!r}")
        key, val = m.group(2), strip_comment(m.group(3))
        if m.group(1):  # 缩进行：fields 字典项
            if target is None:
                raise ValueError(f"field item before any key: {raw!r}")
            if not isinstance(data.get(target), dict):
                data[target] = {}
            data[target][key] = strip_quotes(val)
        else:
            target = key
            if val == "":
                data[key] = None  # 块式，待后续行填充
            elif val == "[]":
                data[key] = []
            elif val == "{}":
                data[key] = {}
            else:
                data[key] = strip_quotes(val)
    return data


def load_plugins():
    """读取全部插件 manifest；返回 (plugins, errors)。"""
    plugins, errors = {}, []
    for name in sorted(os.listdir(PLUGINS_DIR)):
        pdir = os.path.join(PLUGINS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        yml = os.path.join(pdir, "PLUGIN.yaml")
        md = os.path.join(pdir, "PLUGIN.md")
        if not os.path.exists(yml) or not os.path.exists(md):
            errors.append(f"[error] {name}/: PLUGIN.yaml or PLUGIN.md missing")
            continue
        try:
            m = parse_manifest(yml)
        except ValueError as e:
            errors.append(f"[error] {name}/PLUGIN.yaml: {e}")
            continue
        plugins[name] = m
    return plugins, errors


def validate(plugins, errors):
    """合规与依赖检查；错误追加进 errors。"""
    for name, m in sorted(plugins.items()):
        for k in REQUIRED_KEYS:
            if k not in m:
                errors.append(f"[error] {name}/PLUGIN.yaml: missing field {k}")
        if m.get("id") and m["id"] != name:
            errors.append(f"[error] {name}/: id ({m['id']}) != directory name")
        if m.get("version") and not re.fullmatch(r"\d+\.\d+", str(m["version"])):
            errors.append(f"[error] {name}/: version ({m['version']}) not X.Y")
        if m.get("updated") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(m["updated"])):
            errors.append(f"[error] {name}/: updated ({m['updated']}) not YYYY-MM-DD")
        deps = m.get("depends")
        if deps is not None and not isinstance(deps, list):
            errors.append(f"[error] {name}/: depends must be a list")
        # 分层依赖方向：origin/field 是底（零依赖）；derived 只可向下依赖（同层禁依赖）
        layer = m.get("layer")
        if layer not in LAYERS:
            errors.append(f"[error] {name}/: layer ({layer}) must be origin/field/derived")
        elif layer in ("origin", "field") and deps:
            errors.append(f"[error] {name}/ ({layer} is a base layer): depends not allowed ({', '.join(deps)})")
        if not m.get("inject"):
            errors.append(f"[error] {name}/: inject (projection line) empty")
        # 附检契约（可选）：scripts/check.py 存在则必须定义 check(ctx)——AST 静态查，不执行
        cpath = os.path.join(PLUGINS_DIR, name, "scripts", "check.py")
        if os.path.exists(cpath):
            try:
                tree = ast.parse(open(cpath, encoding="utf-8").read())
            except SyntaxError as e:
                errors.append(f"[error] {name}/scripts/check.py syntax error: {e}")
            else:
                if not any(isinstance(n, ast.FunctionDef) and n.name == "check" for n in tree.body):
                    errors.append(f"[error] {name}/scripts/check.py: check(ctx) not defined (audit contract)")
    # 依赖存在性与同层禁依赖
    for name, m in sorted(plugins.items()):
        for dep in m.get("depends") or []:
            if dep not in plugins:
                errors.append(f"[error] {name}/: dependency {dep} not found")
            elif m.get("layer") == "derived" and plugins[dep].get("layer") == "derived":
                errors.append(f"[error] {name}/: dependency {dep} is also derived (same-layer dep forbidden)")
    # 环检测（DFS 三色标记）
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in plugins}

    def dfs(node, path):
        color[node] = GRAY
        for dep in plugins[node].get("depends") or []:
            if dep not in plugins:
                continue
            if color[dep] == GRAY:
                errors.append(f"[error] dependency cycle: {' -> '.join(path + [node, dep])}")
            elif color[dep] == WHITE:
                dfs(dep, path + [node])
        color[node] = BLACK

    for k in sorted(plugins):
        if color[k] == WHITE:
            dfs(k, [])


def _owner_list(owner):
    """owner 值规范化为 id 列表：list 原样，字符串按逗号拆（容忍 [a, b] 形态）。"""
    if isinstance(owner, list):
        vals = [str(v).strip() for v in owner]
    else:
        vals = [v.strip() for v in str(owner).replace("[", "").replace("]", "").split(",")]
    return [v for v in vals if v]


def validate_bindings(plugins, errors):
    """命令-插件绑定：命令 frontmatter owner × 插件 manifest commands 双向一致。"""
    import wikilib

    commands, claimed = [], {}  # claimed: 命令 -> owner 集合（framework 除外）
    for name in sorted(os.listdir(COMMANDS_DIR)):
        cdir = os.path.join(COMMANDS_DIR, name)
        path = os.path.join(cdir, "SKILL.md")
        if not os.path.isdir(cdir) or not os.path.exists(path):
            continue
        commands.append(name)
        fm = wikilib.parse_frontmatter(open(path, encoding="utf-8").read())
        if fm.get("owner") is None:
            errors.append(f"[error] command {name}/: frontmatter missing owner (plugin id or framework)")
            continue
        owners = _owner_list(fm["owner"])
        if "framework" in owners:
            if len(owners) > 1:
                errors.append(f"[error] command {name}/: framework cannot combine with other owners ({', '.join(owners)})")
            continue
        claimed[name] = set(owners)
        for pid in owners:
            if pid not in plugins:
                errors.append(f"[error] command {name}/: owner {pid} is not an installed plugin")
    for pid, m in sorted(plugins.items()):
        cmds = m.get("commands")
        if cmds is None:
            continue
        if not isinstance(cmds, list):
            errors.append(f"[error] {pid}/: commands must be a list")
            continue
        for c in cmds:
            if c not in commands:
                errors.append(f"[error] {pid}/: commands declares missing command {c} (.meta/command/{c}/)")
            elif c not in claimed:
                errors.append(f"[error] command {c}/: {pid} one-sided claim (owner is framework or missing)")
            elif pid not in claimed[c]:
                errors.append(f"[error] command {c}/: {pid} one-sided claim (owner does not include {pid})")
    for c, owners in sorted(claimed.items()):
        for pid in owners:
            if pid in plugins and c not in (plugins[pid].get("commands") or []):
                errors.append(f"[error] command {c}/: owner {pid} not claimed in manifest commands (one-sided)")


def do_audit(plugins, only=None):
    """插件附检：发现式执行各插件 scripts/check.py（契约见模块 docstring）。

    这是「代码注入」的机制形态：插件目录里存在契约合规的附检脚本即自动入列，
    卸载目录移出即自动出列——与 AGENTS.md 注入区同构（在场即注册），但代码
    不做文本拼接（避免命名空间与合并噪音），改为发现 + 调用。
    """
    import wikilib

    pages = list(wikilib.walk_pages(ROOT))  # 单次扫描，全部插件共享（调用节俭）
    ctx = types.SimpleNamespace(root=ROOT, pages=pages)
    counts = {"error": 0, "warning": 0, "info": 0}
    ran = 0
    for pid in sorted(plugins):
        if only and pid != only:
            continue
        cpath = os.path.join(PLUGINS_DIR, pid, "scripts", "check.py")
        if not os.path.exists(cpath):
            continue
        spec = importlib.util.spec_from_file_location(f"plugin_check_{pid}", cpath)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            issues = mod.check(ctx) or []
        except Exception as e:  # 附检脚本自身故障按 error 报告，不拖垮其余插件
            print(f"[error] ({pid}) check script failed: {e}")
            counts["error"] += 1
            ran += 1
            continue
        ran += 1
        for it in issues:
            level = str(it.get("level", "warning"))
            counts[level] = counts.get(level, 0) + 1
            print(f"[{level}] ({pid}) {it.get('message', '')}")
    if ran == 0:
        print("[audit] no plugin carries scripts/check.py (optional contract; currently semantic-only)")
        return 0
    print(f"[audit] {ran} plugins, error {counts['error']} / warning {counts.get('warning', 0)} / info {counts.get('info', 0)}")
    return 1 if counts["error"] else 0


def do_inject(plugins):
    """自 manifests 重建 AGENTS.md 注入区（保留前置说明，块按层分组再按 id 排序，幂等）。"""
    text = open(AGENTS_MD, encoding="utf-8").read()
    m = re.search(re.escape(INJECT_START) + r"\n(.*?)" + re.escape(INJECT_END), text, re.S)
    if not m:
        print("[error] AGENTS.md: inject markers (wiki-inject:start/end) not found")
        return False
    region = m.group(1)
    first = region.find("<!-- plugin:")
    preamble = region[:first].rstrip() if first != -1 else region.rstrip()
    blocks = []
    for pid in ordered_plugins(plugins):
        ver = plugins[pid].get("version")
        line = plugins[pid].get("inject", "")
        blocks.append(f"<!-- plugin:{pid} v{ver} -->\n- {line}\n<!-- /plugin:{pid} -->")
    new_region = preamble + "\n\n" + "\n\n".join(blocks) + "\n\n"
    if new_region == region:
        print("[inject] region unchanged")
        return True
    open(AGENTS_MD, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + new_region + text[m.end(1):]
    )
    print(f"[inject] rebuilt ({len(blocks)} plugin blocks)")
    return True


def do_check_inject(plugins):
    """自各 PLUGIN.md「检查」节重建 check 命令注入区（在场即注册，幂等）。

    与 AGENTS.md 注入区同构：PLUGIN.md 是本体，check 块是投影——改检查规则
    改 PLUGIN.md「检查」节，本投影与手写块的漂移就此消失。
    """
    if not os.path.exists(CHECK_SKILL):
        print("[check-inject] check command absent, skipped")
        return True
    text = open(CHECK_SKILL, encoding="utf-8").read()
    m = re.search(re.escape(CHECK_INJECT_START) + r"\n(.*?)" + re.escape(CHECK_INJECT_END), text, re.S)
    if not m:
        print("[error] check/SKILL.md: inject markers (check-inject:start/end) not found")
        return False
    blocks = []
    for pid in ordered_plugins(plugins):
        sec = CHECK_SECTION_RE.search(open(os.path.join(PLUGINS_DIR, pid, "PLUGIN.md"), encoding="utf-8").read())
        if sec and sec.group(1).strip():
            blocks.append(f"<!-- check:{pid} -->\n{sec.group(1).strip()}\n<!-- /check:{pid} -->")
    new_region = "\n\n".join(blocks) + "\n"
    if new_region == m.group(1):
        print("[check-inject] unchanged")
        return True
    open(CHECK_SKILL, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + new_region + text[m.end(1):]
    )
    print(f"[check-inject] rebuilt ({len(blocks)} plugin blocks)")
    return True


def do_registry(plugins):
    """自 manifests 的 fields 重建 registry.yaml 插件段（protocol / reserved 段不动）。"""
    text = open(REGISTRY, encoding="utf-8").read()
    m = re.search(r"^plugins:\n(.*?)^reserved:", text, re.S | re.M)
    if not m:
        print("[error] registry.yaml: plugins:/reserved: section structure not found")
        return False
    lines = []
    for pid in sorted(plugins):
        fields = plugins[pid].get("fields")
        if not fields:
            continue  # 无自有字段的插件不入注册表插件段
        lines.append(f"  {pid}:")
        for f in sorted(fields):
            lines.append(f"    {f}:")
            lines.append(f"      note: {fields[f]}")
    body = "\n".join(lines) + "\n\n"
    if body == m.group(1):
        print("[registry] plugin section unchanged")
        return True
    open(REGISTRY, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + body + text[m.end(1):]
    )
    print("[registry] plugin section rebuilt")
    return True


def do_deploy():
    """同步 .meta/command/*/SKILL.md → .agents/skills/*/SKILL.md；孤儿副本仅报告。"""
    names = sorted(
        d for d in os.listdir(COMMANDS_DIR)
        if os.path.isdir(os.path.join(COMMANDS_DIR, d))
    )
    changed = 0
    for name in names:
        src = os.path.join(COMMANDS_DIR, name, "SKILL.md")
        if not os.path.exists(src):
            print(f"[warning] command {name}/: SKILL.md missing")
            continue
        dst_dir = os.path.join(SKILLS_DIR, name)
        dst = os.path.join(dst_dir, "SKILL.md")
        os.makedirs(dst_dir, exist_ok=True)
        if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
            shutil.copyfile(src, dst)
            changed += 1
            print(f"[deploy] synced {name}/SKILL.md")
    if os.path.isdir(SKILLS_DIR):
        for d in sorted(os.listdir(SKILLS_DIR)):
            if d not in names and os.path.isdir(os.path.join(SKILLS_DIR, d)):
                print(f"[warning] orphan copy .agents/skills/{d}/ (master gone; deletion belongs to human)")
    if not changed:
        print("[deploy] all in sync")
    return True


def do_ls(plugins):
    lay_names = {"origin": "origin", "field": "field", "derived": "derived"}
    for lay in LAYERS:
        names = [p for p in sorted(plugins) if plugins[p].get("layer") == lay]
        if not names:
            continue
        print(f"[{lay_names[lay]}]")
        for pid in names:
            deps = ", ".join(plugins[pid].get("depends") or []) or "—"
            cmds = ", ".join(plugins[pid].get("commands") or []) or "—"
            print(f"  {pid:<10} {plugins[pid].get('version', '?'):<6} 依赖 {deps}；命令 {cmds}")
    others = [p for p in sorted(plugins) if plugins[p].get("layer") not in LAYERS]
    if others:
        print("[unlayered]")
        for pid in others:
            print(f"  {pid:<10} {plugins[pid].get('version', '?'):<6} ?")
    print(f"{len(plugins)} plugins (.meta/plugins/; base layers zero-dep, derived depends downward only)")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    plugins, errors = load_plugins()
    if cmd == "ls":
        do_ls(plugins)
        if errors:
            print(f"[warning] {len(errors)} manifest load errors — run validate for details")
        return 0
    if cmd == "audit":
        for e in errors:
            print(e)
        return do_audit(plugins, sys.argv[2] if len(sys.argv) > 2 else None)
    if cmd not in ("validate", "inject", "registry", "deploy", "all"):
        print(__doc__)
        return 2
    validate(plugins, errors)
    validate_bindings(plugins, errors)
    for e in errors:
        print(e)
    if errors:
        print(f"[result] validation failed ({len(errors)} errors) — mechanical actions blocked")
        return 1
    print(f"[validate] all {len(plugins)} plugins passed (fields / id match / layer valid / dep direction / acyclic / command bindings)")
    if cmd in ("inject", "all"):
        if not do_inject(plugins):
            return 1
        if not do_check_inject(plugins):
            return 1
    if cmd in ("registry", "all"):
        if not do_registry(plugins):
            return 1
    if cmd in ("deploy", "all"):
        if not do_deploy():
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
