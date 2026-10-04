#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""language 插件附检：声明页存在性、领地走位、terms 空值。

声明页缺席 = 默认姿态容忍（合法，info）；terms 值空白即登记瑕疵。
"""


def check(ctx):
    issues = []
    decl = False
    for rel, fm, _body in ctx.pages:
        if fm.get("type") == "language" and rel != "language.md":
            issues.append({"level": "error", "message": f"{rel}：type: language 落声明页之外（领地走位）"})
        if rel == "language.md":
            decl = True
            terms = fm.get("terms") or {}
            for k, v in terms.items():
                if not str(v).strip():
                    issues.append({"level": "warning", "message": f"terms 空值：{k}（译名缺失，补齐或移除）"})
    if not decl:
        issues.append({"level": "info", "message": "无行文声明页（默认姿态容忍）"})
    return issues
