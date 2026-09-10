#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link 插件附检：机械项（断链 / 乱码 / 别名歧义 / 孤儿 / related 单向）。

入链密度 top 榜（hub 涌现依据）是分析项，归 check 命令语义项。
概念页判定与 pipeline 同构：保留名（index/log）、wiki 根派生页（hot/tags）、
archive/ 子树不算链接源，也不受图检查（派生页链接一切，否则孤儿永不触发）。
"""
import re

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
RESERVED_NAMES = {"index.md", "log.md"}
ROOT_DERIVED = {"hot.md", "tags.md"}


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _name_of(rel):
    return rel[:-3] if rel.endswith(".md") else rel


def _concept(rel):
    d, _, fn = rel.rpartition("/")
    if fn in RESERVED_NAMES:
        return False
    if d == "" and fn in ROOT_DERIVED:
        return False
    return not (rel.startswith("archive/") or d.startswith("archive/") or d == "archive")


def _target(text):
    """related 项或 wikilink 文本 → 目标全名（容忍 [[x|显示]] 与裸名两种形态）。"""
    return str(text).strip().lstrip("[").split("|")[0].strip().rstrip("]")


def check(ctx):
    issues = []
    pages = list(ctx.pages)
    names = {_name_of(rel) for rel, _fm, _b in pages}
    # 别名表与二义（error：让 [[别名]] 解析不确定）
    alias_map = {}
    for rel, fm, _b in pages:
        for a in _as_list(fm.get("aliases")):
            alias_map.setdefault(str(a).strip(), set()).add(_name_of(rel))
    for a, owners in sorted(alias_map.items()):
        if len(owners) > 1:
            issues.append({"级别": "error", "消息": f"别名 {a!r} 二义：{'、'.join(sorted(owners))}——解析不确定，须裁决"})
    referenced, related_map = set(), {}
    for rel, fm, body in pages:
        if not _concept(rel):
            continue
        src = _name_of(rel)
        for m in WIKILINK_RE.finditer(body):
            t = m.group(1).strip()
            if "\ufffd" in t:
                issues.append({"级别": "error", "消息": f"{rel}：乱码链接 [[{m.group(1)}]]"})
            elif t not in names and t not in alias_map:
                issues.append({"级别": "warning", "消息": f"{rel}：断链 [[{t}]]（既非页面全名，也非任何 aliases）"})
            referenced.add(t)
        rels = [_target(r) for r in _as_list(fm.get("related"))]
        related_map[src] = {t for t in rels if t}
        for t in rels:
            if "\ufffd" in t:
                issues.append({"级别": "error", "消息": f"{rel}：related 乱码项 {t!r}"})
            elif t not in names and t not in alias_map:
                issues.append({"级别": "warning", "消息": f"{rel}：related 断链 [[{t}]]"})
            referenced.add(t)
    # 孤儿（无入链且无 related 引用；源只计概念页）
    for rel, _fm, _b in pages:
        if not _concept(rel):
            continue
        if _name_of(rel) not in referenced:
            issues.append({"级别": "warning", "消息": f"{rel}：孤儿页（无入链且无 related 引用）"})
    # related 单向（信息：不对称提示，非错误）
    for src, rels in sorted(related_map.items()):
        for t in sorted(rels):
            if t in related_map and src not in related_map[t]:
                issues.append({"级别": "信息", "消息": f"{src}：related 单向（列出 [[{t}]]，对方未回列）"})
    return issues
