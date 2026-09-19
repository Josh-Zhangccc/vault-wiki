#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link 插件附检：机械项（断链 / 乱码 / 别名歧义 / 孤儿 / related 单向）。

入链密度 top 榜（hub 涌现依据）是分析项，归 check 命令语义项。
概念页判定与 pipeline 同构：保留名（index/log）、wiki 根派生页（hot/tags）、
archive/ 子树与 tmp/ 临时区不算链接源，也不受图检查（派生页链接一切，否则孤儿
永不触发；草稿断链 = 尚未写下，转正时闭合）。
hot 是唯一手写链接的派生页：断链受检，但不作入链源、不入孤儿图。
领地值页（registry type.values 除 session——机械登记类）暂无入链是登记常态：
孤儿降为信息级，原生页（notes 知识页）保持 warning。领地值集动态读 registry，
新领地类型自动覆盖，免逐类型维护。
"""
import os
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
    if rel.startswith("tmp/") or d.startswith("tmp/") or d == "tmp":
        return False  # 临时区：不作链接源、不受图检查（草稿断链豁免）
    return not (rel.startswith("archive/") or d.startswith("archive/") or d == "archive")


def _target(text):
    """related 项或 wikilink 文本 → 目标全名（容忍 [[x|显示]] 与裸名两种形态）。"""
    return str(text).strip().lstrip("[").split("|")[0].strip().rstrip("]")


TERRITORY_LABELS = {"source": "代理页", "lark": "指针页", "calendar": "时间页",
                    "structure": "声明页", "todo": "委托页", "profile": "画像页", "project": "项目页"}


def _territory_types(root):
    """registry type.values（领地值封闭集）动态读取；session 除外（知识骨干，孤儿提示有意义）。"""
    try:
        text = open(os.path.join(root, ".meta", "protocol", "registry.yaml"), encoding="utf-8").read()
        m = re.search(r"values: \[([^\]]+)\]", text)
        return {v.strip() for v in m.group(1).split(",") if v.strip()} - {"session"}
    except OSError:
        return set(TERRITORY_LABELS)


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
            issues.append({"level": "error", "message": f"别名 {a!r} 二义：{'、'.join(sorted(owners))}——解析不确定，须裁决"})
    referenced, related_map = set(), {}
    for rel, fm, body in pages:
        if not _concept(rel):
            continue
        src = _name_of(rel)
        for m in WIKILINK_RE.finditer(body):
            t = m.group(1).strip()
            if "\ufffd" in t:
                issues.append({"level": "error", "message": f"{rel}：乱码链接 [[{m.group(1)}]]"})
            elif t not in names and t not in alias_map:
                issues.append({"level": "warning", "message": f"{rel}：断链 [[{t}]]（既非页面全名，也非任何 aliases）"})
            referenced.add(t)
        rels = [_target(r) for r in _as_list(fm.get("related"))]
        related_map[src] = {t for t in rels if t}
        for t in rels:
            if "\ufffd" in t:
                issues.append({"level": "error", "message": f"{rel}：related 乱码项 {t!r}"})
            elif t not in names and t not in alias_map:
                issues.append({"level": "warning", "message": f"{rel}：related 断链 [[{t}]]"})
            referenced.add(t)
    # hot：手写链接面（断链受检；不作入链源、不入孤儿图）
    for rel, _fm, body in pages:
        if _name_of(rel) != "hot":
            continue
        for m in WIKILINK_RE.finditer(body):
            t = m.group(1).strip()
            if "\ufffd" in t:
                issues.append({"level": "error", "message": f"{rel}：乱码链接 [[{m.group(1)}]]"})
            elif t not in names and t not in alias_map:
                issues.append({"level": "warning", "message": f"{rel}：hot 断链 [[{t}]]（手写摘要链接失效）"})
    # 孤儿（无入链且无 related 引用；源只计概念页；领地值登记页降 info）
    territory = _territory_types(ctx.root)
    for rel, fm, _b in pages:
        if not _concept(rel):
            continue
        if _name_of(rel) not in referenced:
            ptype = fm.get("type")
            if ptype in territory:
                label = TERRITORY_LABELS.get(ptype, "领地页")
                issues.append({"level": "info", "message": f"{rel}：{label}暂无入链（登记常态，不告警）"})
            else:
                issues.append({"level": "warning", "message": f"{rel}：孤儿页（无入链且无 related 引用）"})
    # related 单向（信息：不对称提示，非错误）
    for src, rels in sorted(related_map.items()):
        for t in sorted(rels):
            if t in related_map and src not in related_map[t]:
                issues.append({"level": "info", "message": f"{src}：related 单向（列出 [[{t}]]，对方未回列）"})
    return issues
