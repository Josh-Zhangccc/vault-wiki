#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag 插件附检：机械项（单页数量上限 / 复述 type）。

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
            issues.append({"级别": "warning", "消息": f"{rel}：{len(tags)} 个 tag（>5 软上限）"})
        ptype = fm.get("type")
        if ptype and ptype in tags:
            issues.append({"级别": "warning", "消息": f"{rel}：tag 复述 type（{ptype}）"})
    return issues
