#!/usr/bin/env python3
"""test 插件：静态结构校验（合规三级检查之第一级）。

用法: python check.py [<plugins 目录，默认本仓库 .meta/plugins>]

只支持 manifest 约定的最小 YAML 子集（顶层标量键值、单行列表 [a, b]、
一层 entry 缩进、# 注释行与行尾注释），不引入第三方依赖。
"""
import re
import sys
from pathlib import Path

REQUIRED = ["type", "id", "version", "class", "scopes", "depends", "status", "updated"]
VALID_CLASS = {"bearing", "normal"}
VALID_STATUS = {"draft", "stable", "deprecated"}
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def strip_comment(s):
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def parse_value(s):
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [v.strip() for v in inner.split(",") if v.strip()] if inner else []
    return s


def parse_manifest(path):
    """返回 (fields, entry)；解析失败返回 (None, None, 错误信息)。"""
    fields, entry, target = {}, None, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = strip_comment(raw)
        if not line:
            continue
        m = KEY_RE.match(line)
        if not m:
            return None, None, f"无法解析的行: {raw!r}"
        key, rest = m.group(1), m.group(2).strip()
        indented = raw[0].isspace()
        if indented and target is not None:
            target[key] = parse_value(rest)
        elif not indented:
            if rest == "":
                if key == "entry":
                    entry = target = {}
                else:
                    fields[key], target = None, None
            else:
                fields[key] = parse_value(rest)
                target = None
        else:
            return None, None, f"缩进出现在 entry 块之外: {raw!r}"
    return fields, entry, None


def check_depends(plugins, errors):
    """依赖存在性、承重件不依赖、有向无环。同层/向上依赖需层信息，协议定稿后补。"""
    def visit(pid, stack):
        if pid in stack:
            chain = " -> ".join(stack[stack.index(pid):] + [pid])
            errors.append(f"[error] {pid}: 依赖成环 {chain}")
            return
        deps = plugins[pid][1].get("depends") or []
        for dep in deps:
            if dep not in plugins:
                errors.append(f"[error] {pid}: 依赖的插件 {dep} 不存在")
                continue
            if plugins[pid][1].get("class") == "bearing":
                errors.append(f"[error] {pid}: 承重件不得依赖任何插件（分层的底）")
            visit(dep, stack + [pid])

    for pid in plugins:
        visit(pid, [])


def main():
    plugins_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    if not plugins_dir.is_dir():
        print(f"[error] 插件目录不存在: {plugins_dir}")
        sys.exit(1)

    errors, plugins = [], {}
    for d in sorted(p for p in plugins_dir.iterdir() if p.is_dir()):
        mf = d / "PLUGIN.yaml"
        if not mf.exists():
            errors.append(f"[error] {d.name}: 缺少 PLUGIN.yaml（未成形插件）")
            continue
        fields, entry, err = parse_manifest(mf)
        if err:
            errors.append(f"[error] {d.name}: manifest 解析失败：{err}")
            continue
        for key in REQUIRED:
            if key not in fields or fields[key] is None:
                errors.append(f"[error] {d.name}: 缺少必填字段 {key}")
        for key in ("scopes", "depends"):
            if key in fields and not isinstance(fields[key], list):
                errors.append(f"[error] {d.name}: {key} 应为列表")
        if fields.get("class") not in VALID_CLASS:
            errors.append(f"[error] {d.name}: class 取值非法（应为 bearing/normal）")
        if fields.get("status") not in VALID_STATUS:
            errors.append(f"[error] {d.name}: status 取值非法（应为 draft/stable/deprecated）")
        pid = fields.get("id")
        if pid != d.name:
            errors.append(f"[error] {d.name}: id '{pid}' 与目录名不一致")
        if pid and pid in plugins:
            errors.append(f"[error] {d.name}: id '{pid}' 与 {plugins[pid][0].name} 重复")
        entry = entry or {}
        if not entry.get("doc"):
            errors.append(f"[error] {d.name}: entry.doc 必填")
        elif not (d / entry["doc"]).exists():
            errors.append(f"[error] {d.name}: entry.doc 指向的 {entry['doc']} 不存在")
        for s in entry.get("scripts", []):
            if not (d / s).exists():
                errors.append(f"[error] {d.name}: entry.scripts 指向的 {s} 不存在")
        if pid and pid not in plugins:
            plugins[pid] = (d, fields)

    # TODO（协议定稿后）：与注册表双向核对（未登记视为不存在 / 幽灵插件）
    check_depends(plugins, errors)

    for pid, (d, _) in sorted(plugins.items()):
        print(f"[ok] {pid} ({d.name})" if not errors else f"[checked] {pid} ({d.name})")
    for e in errors:
        print(e)
    print(f"\n{'FAIL' if errors else 'PASS'}: {len(plugins)} 个插件, {len(errors)} 个错误")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
