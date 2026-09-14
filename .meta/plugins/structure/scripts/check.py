#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""structure 插件附检：结构声明页存在性、声明与 vault 实际顶层目录 diff、领地走位。

声明页缺席 = 平铺容忍（合法，info）；diff 只对顶层目录，顶层散文件是平铺位不受约束。
"""
import os


def check(ctx):
    issues = []
    # 领地走位：type: structure 只许 wiki/structure.md
    decl = None
    for rel, fm, _body in ctx.pages:
        if fm.get("type") == "structure" and rel != "structure.md":
            issues.append({"level": "error", "message": f"{rel}：type: structure 落声明页之外（领地走位）"})
        if rel == "structure.md":
            decl = fm.get("structure") or {}
    if decl is None:
        issues.append({"level": "info", "message": "无结构声明页（平铺容忍）"})
        return issues
    vroot = os.path.join(ctx.root, "vault")
    if not os.path.isdir(vroot):
        return issues
    actual = {d + "/" for d in os.listdir(vroot)
              if os.path.isdir(os.path.join(vroot, d)) and not d.startswith(".")}
    declared = {str(k).strip() for k in decl}
    for d in sorted(actual - declared):
        issues.append({"level": "warning", "message": f"vault 顶层目录未声明：{d}（补声明或归位）"})
    for d in sorted(declared - actual):
        issues.append({"level": "warning", "message": f"声明指向不存在的目录：{d}（声明过时，同步或删除）"})
    return issues
