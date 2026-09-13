#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag 插件附检：机械项（单页数量上限 / 复述 type / 层级深度）。

近重复 tag 是语义项（跨语言同义词字符串层面不可判），归 check 命令。
"""


def check(ctx):
    issues = []
    for rel, fm, body in ctx.pages:
        tags = fm.get("tags")
        if tags is None:
            continue
        if not isinstance(tags, list):
            tags = [tags]
        if len(tags) > 5:
            issues.append({"level": "warning", "message": f"{rel}：{len(tags)} 个 tag（>5 软上限）"})
        ptype = fm.get("type")
        if ptype and ptype in tags:
            issues.append({"level": "warning", "message": f"{rel}：tag 复述 type（{ptype}）"})
        for t in tags:
            s = str(t)
            if "/" in s:
                parts = s.split("/")
                if len(parts) > 2 or any(not p.strip() for p in parts):
                    issues.append({"level": "warning", "message": f"{rel}：tag 层级超限或空段（{s}，父/子 ≤2）"})
    return issues
