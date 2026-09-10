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
  python .meta/scripts/plugin_cli.py inject      # 重建 AGENTS.md 注入区（幂等）
  python .meta/scripts/plugin_cli.py registry    # 重建 registry.yaml 插件段（幂等）
  python .meta/scripts/plugin_cli.py deploy      # 同步命令部署副本（幂等）
  python .meta/scripts/plugin_cli.py all         # validate + inject + registry + deploy

manifest 最小 YAML 子集：顶层 `key: value`、`key: []`、块式列表（`  - 项`）、
一层字段字典（`  name: 描述`）；双引号包裹的值去引号；行内注释（` #` 起）剥离。

分层（layer，三值）与依赖方向：
- origin（出身：拥有页面领地）与 field（字段：拥有跨页 frontmatter 字段）是底，零依赖
- derived（派生：拥有派生物与写路径义务）居上，只可依赖 origin/field，同层禁依赖

插件附检契约（scripts/check.py，可选）：
- 必须定义 check(ctx)，返回 issue 列表：{"级别": "error"|"warning"|"信息", "消息": str}
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

# manifest 八字段（id / version / layer / depends / updated / attachment / fields / inject）
REQUIRED_KEYS = ["id", "version", "layer", "depends", "updated", "attachment", "fields", "inject"]
LAYERS = ("origin", "field", "derived")
INJECT_START = "<!-- wiki-inject:start -->"
INJECT_END = "<!-- wiki-inject:end -->"


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
                raise ValueError(f"列表项出现在任何键之前: {raw!r}")
            item = strip_quotes(strip_comment(raw.strip()[2:]))
            if not isinstance(data.get(target), list):
                data[target] = []
            data[target].append(item)
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not m:
            raise ValueError(f"无法解析的行: {raw!r}")
        key, val = m.group(2), strip_comment(m.group(3))
        if m.group(1):  # 缩进行：fields 字典项
            if target is None:
                raise ValueError(f"字段项出现在任何键之前: {raw!r}")
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
            errors.append(f"[错误] {name}/：PLUGIN.yaml 或 PLUGIN.md 缺失")
            continue
        try:
            m = parse_manifest(yml)
        except ValueError as e:
            errors.append(f"[错误] {name}/PLUGIN.yaml：{e}")
            continue
        plugins[name] = m
    return plugins, errors


def validate(plugins, errors):
    """合规与依赖检查；错误追加进 errors。"""
    for name, m in sorted(plugins.items()):
        for k in REQUIRED_KEYS:
            if k not in m:
                errors.append(f"[错误] {name}/PLUGIN.yaml：缺字段 {k}")
        if m.get("id") and m["id"] != name:
            errors.append(f"[错误] {name}/：id（{m['id']}）与目录名不一致")
        if m.get("version") and not re.fullmatch(r"\d+\.\d+", str(m["version"])):
            errors.append(f"[错误] {name}/：version（{m['version']}）不符合 X.Y 格式")
        if m.get("updated") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(m["updated"])):
            errors.append(f"[错误] {name}/：updated（{m['updated']}）不符合 YYYY-MM-DD")
        deps = m.get("depends")
        if deps is not None and not isinstance(deps, list):
            errors.append(f"[错误] {name}/：depends 应为列表")
        # 分层依赖方向：origin/field 是底（零依赖）；derived 只可向下依赖（同层禁依赖）
        layer = m.get("layer")
        if layer not in LAYERS:
            errors.append(f"[错误] {name}/：layer（{layer}）须为 origin/field/derived")
        elif layer in ("origin", "field") and deps:
            errors.append(f"[错误] {name}/（{layer} 层为底）：不得声明依赖（{', '.join(deps)}）")
        if not m.get("inject"):
            errors.append(f"[错误] {name}/：inject（注入区投影行）为空")
        # 附检契约（可选）：scripts/check.py 存在则必须定义 check(ctx)——AST 静态查，不执行
        cpath = os.path.join(PLUGINS_DIR, name, "scripts", "check.py")
        if os.path.exists(cpath):
            try:
                tree = ast.parse(open(cpath, encoding="utf-8").read())
            except SyntaxError as e:
                errors.append(f"[错误] {name}/scripts/check.py 语法错误：{e}")
            else:
                if not any(isinstance(n, ast.FunctionDef) and n.name == "check" for n in tree.body):
                    errors.append(f"[错误] {name}/scripts/check.py 未定义 check(ctx)（附检契约）")
    # 依赖存在性与同层禁依赖
    for name, m in sorted(plugins.items()):
        for dep in m.get("depends") or []:
            if dep not in plugins:
                errors.append(f"[错误] {name}/：依赖的 {dep} 不存在")
            elif m.get("layer") == "derived" and plugins[dep].get("layer") == "derived":
                errors.append(f"[错误] {name}/：依赖的 {dep} 同为 derived 层（同层禁依赖）")
    # 环检测（DFS 三色标记）
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in plugins}

    def dfs(node, path):
        color[node] = GRAY
        for dep in plugins[node].get("depends") or []:
            if dep not in plugins:
                continue
            if color[dep] == GRAY:
                errors.append(f"[错误] 依赖成环：{' -> '.join(path + [node, dep])}")
            elif color[dep] == WHITE:
                dfs(dep, path + [node])
        color[node] = BLACK

    for k in sorted(plugins):
        if color[k] == WHITE:
            dfs(k, [])


def do_audit(plugins, only=None):
    """插件附检：发现式执行各插件 scripts/check.py（契约见模块 docstring）。

    这是「代码注入」的机制形态：插件目录里存在契约合规的附检脚本即自动入列，
    卸载目录移出即自动出列——与 AGENTS.md 注入区同构（在场即注册），但代码
    不做文本拼接（避免命名空间与合并噪音），改为发现 + 调用。
    """
    import wikilib

    pages = list(wikilib.walk_pages(ROOT))  # 单次扫描，全部插件共享（调用节俭）
    ctx = types.SimpleNamespace(root=ROOT, pages=pages)
    counts = {"error": 0, "warning": 0, "信息": 0}
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
            print(f"[error] ({pid}) 附检脚本执行失败：{e}")
            counts["error"] += 1
            ran += 1
            continue
        ran += 1
        for it in issues:
            level = str(it.get("级别", "warning"))
            counts[level] = counts.get(level, 0) + 1
            print(f"[{level}] ({pid}) {it.get('消息', '')}")
    if ran == 0:
        print("[附检] 无插件携带 scripts/check.py（可选契约，当前为纯语义检查）")
        return 0
    print(f"[附检] {ran} 个插件，error {counts['error']} / warning {counts.get('warning', 0)} / 信息 {counts.get('信息', 0)}")
    return 1 if counts["error"] else 0


def do_inject(plugins):
    """自 manifests 重建 AGENTS.md 注入区（保留前置说明，块按层分组再按 id 排序，幂等）。"""
    text = open(AGENTS_MD, encoding="utf-8").read()
    m = re.search(re.escape(INJECT_START) + r"\n(.*?)" + re.escape(INJECT_END), text, re.S)
    if not m:
        print("[错误] AGENTS.md 未找到注入区标记块（wiki-inject:start/end）")
        return False
    region = m.group(1)
    first = region.find("<!-- plugin:")
    preamble = region[:first].rstrip() if first != -1 else region.rstrip()
    blocks = []
    for pid in sorted(plugins, key=lambda p: (LAYERS.index(plugins[p]["layer"]) if plugins[p].get("layer") in LAYERS else len(LAYERS), p)):
        ver = plugins[pid].get("version")
        line = plugins[pid].get("inject", "")
        blocks.append(f"<!-- plugin:{pid} v{ver} -->\n- {line}\n<!-- /plugin:{pid} -->")
    new_region = preamble + "\n\n" + "\n\n".join(blocks) + "\n\n"
    if new_region == region:
        print("[注入] 注入区一致，无变化")
        return True
    open(AGENTS_MD, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + new_region + text[m.end(1):]
    )
    print(f"[注入] 已重建（{len(blocks)} 个插件块）")
    return True


def do_registry(plugins):
    """自 manifests 的 fields 重建 registry.yaml 插件段（protocol / reserved 段不动）。"""
    text = open(REGISTRY, encoding="utf-8").read()
    m = re.search(r"^plugins:\n(.*?)^reserved:", text, re.S | re.M)
    if not m:
        print("[错误] registry.yaml 未找到 plugins: / reserved: 段结构")
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
        print("[注册表] 插件段一致，无变化")
        return True
    open(REGISTRY, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + body + text[m.end(1):]
    )
    print("[注册表] 插件段已重建")
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
            print(f"[警告] 命令 {name}/ 缺 SKILL.md")
            continue
        dst_dir = os.path.join(SKILLS_DIR, name)
        dst = os.path.join(dst_dir, "SKILL.md")
        os.makedirs(dst_dir, exist_ok=True)
        if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
            shutil.copyfile(src, dst)
            changed += 1
            print(f"[副本] 已同步 {name}/SKILL.md")
    if os.path.isdir(SKILLS_DIR):
        for d in sorted(os.listdir(SKILLS_DIR)):
            if d not in names and os.path.isdir(os.path.join(SKILLS_DIR, d)):
                print(f"[警告] 孤儿副本 .agents/skills/{d}/（主本已不存在，删除属人）")
    if not changed:
        print("[副本] 全部一致")
    return True


def do_ls(plugins):
    lay_names = {"origin": "origin 出身", "field": "field 字段", "derived": "derived 派生"}
    for lay in LAYERS:
        names = [p for p in sorted(plugins) if plugins[p].get("layer") == lay]
        if not names:
            continue
        print(f"[{lay_names[lay]}]")
        for pid in names:
            deps = ", ".join(plugins[pid].get("depends") or []) or "—"
            print(f"  {pid:<10} {plugins[pid].get('version', '?'):<6} {deps}")
    others = [p for p in sorted(plugins) if plugins[p].get("layer") not in LAYERS]
    if others:
        print("[未分层]")
        for pid in others:
            print(f"  {pid:<10} {plugins[pid].get('version', '?'):<6} ?")
    print(f"共 {len(plugins)} 个插件（.meta/plugins/；底层零依赖，derived 只向下依赖）")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    plugins, errors = load_plugins()
    if cmd == "ls":
        do_ls(plugins)
        if errors:
            print(f"[警告] {len(errors)} 个 manifest 加载错误——运行 validate 查看明细")
        return 0
    if cmd == "audit":
        for e in errors:
            print(e)
        return do_audit(plugins, sys.argv[2] if len(sys.argv) > 2 else None)
    if cmd not in ("validate", "inject", "registry", "deploy", "all"):
        print(__doc__)
        return 2
    validate(plugins, errors)
    for e in errors:
        print(e)
    if errors:
        print(f"[结果] 合规检查未通过（{len(errors)} 项错误）——阻断后续机械动作")
        return 1
    print(f"[合规] {len(plugins)} 个插件全部通过（八字段 / id 一致 / layer 合法 / 依赖方向 / 无环）")
    if cmd in ("inject", "all"):
        if not do_inject(plugins):
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
