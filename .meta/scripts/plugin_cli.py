#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault-wiki 插件生命周期机械核心（装卸 / 合规 / 依赖 / 注入 / 注册表 / 副本同步）。

定位（见 .meta/protocol/actions.md 执行原则）：确定性的结构操作交给本脚本，
语义判断交给 LLM。脚本只碰四处：插件目录进出、AGENTS.md 注入区标记块、
registry.yaml 插件段、.agents/skills/ 命令副本；protocol / reserved 段与手写区永不动。

用法:
  python .meta/scripts/plugin_cli.py ls          # 清单 + 依赖图
  python .meta/scripts/plugin_cli.py validate    # 合规与依赖检查（只读，错误退出码 1）
  python .meta/scripts/plugin_cli.py inject      # 重建 AGENTS.md 注入区（幂等）
  python .meta/scripts/plugin_cli.py registry    # 重建 registry.yaml 插件段（幂等）
  python .meta/scripts/plugin_cli.py deploy      # 同步命令部署副本（幂等）
  python .meta/scripts/plugin_cli.py all         # validate + inject + registry + deploy

manifest 最小 YAML 子集：顶层 `key: value`、`key: []`、块式列表（`  - 项`）、
一层字段字典（`  name: 描述`）；双引号包裹的值去引号；# 注释行跳过。
"""
import os
import re
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLUGINS_DIR = os.path.join(ROOT, ".meta", "plugins")
COMMANDS_DIR = os.path.join(ROOT, ".meta", "command")
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")
AGENTS_MD = os.path.join(ROOT, "AGENTS.md")
REGISTRY = os.path.join(ROOT, ".meta", "protocol", "registry.yaml")

# manifest 七字段（id / version / depends / updated / attachment / fields / inject）
REQUIRED_KEYS = ["id", "version", "depends", "updated", "attachment", "fields", "inject"]
INJECT_START = "<!-- wiki-inject:start -->"
INJECT_END = "<!-- wiki-inject:end -->"


def strip_quotes(s):
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def parse_manifest(path):
    """解析 manifest 的最小 YAML 子集；失败抛出 ValueError。"""
    data, target = {}, None
    for raw in open(path, encoding="utf-8").read().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") or raw.startswith("- "):
            item = strip_quotes(raw.strip()[2:].strip())
            if not isinstance(data.get(target), list):
                data[target] = []
            data[target].append(item)
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not m:
            raise ValueError(f"无法解析的行: {raw!r}")
        key, val = m.group(2), m.group(3).strip()
        if m.group(1):  # 缩进行：fields 字典项
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
        if not m.get("inject"):
            errors.append(f"[错误] {name}/：inject（注入区投影行）为空")
    # 依赖存在性
    for name, m in sorted(plugins.items()):
        for dep in m.get("depends") or []:
            if dep not in plugins:
                errors.append(f"[错误] {name}/：依赖的 {dep} 不存在")
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


def do_inject(plugins):
    """自 manifests 重建 AGENTS.md 注入区（保留前置说明，块按 id 排序，幂等）。"""
    text = open(AGENTS_MD, encoding="utf-8").read()
    m = re.search(re.escape(INJECT_START) + r"\n(.*?)" + re.escape(INJECT_END), text, re.S)
    if not m:
        print("[错误] AGENTS.md 未找到注入区标记块（wiki-inject:start/end）")
        return False
    region = m.group(1)
    first = region.find("<!-- plugin:")
    preamble = region[:first].rstrip() if first != -1 else region.rstrip()
    blocks = []
    for pid in sorted(plugins):
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
    print(f"{'id':<10} {'版本':<6} 依赖")
    for pid in sorted(plugins):
        deps = ", ".join(plugins[pid].get("depends") or []) or "—"
        print(f"{pid:<10} {plugins[pid].get('version', '?'):<6} {deps}")
    print(f"共 {len(plugins)} 个插件（.meta/plugins/）")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    plugins, errors = load_plugins()
    if cmd == "ls":
        do_ls(plugins)
        return 0
    if cmd not in ("validate", "inject", "registry", "deploy", "all"):
        print(__doc__)
        return 2
    validate(plugins, errors)
    for e in errors:
        print(e)
    if errors:
        print(f"[结果] 合规检查未通过（{len(errors)} 项错误）——阻断后续机械动作")
        return 1
    print(f"[合规] {len(plugins)} 个插件全部通过（七字段 / id 一致 / 依赖存在 / 无环）")
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
