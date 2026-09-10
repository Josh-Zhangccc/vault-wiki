#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""log 插件附检：机械项（条目日期契约）。

历史条目被修改的审计靠 git 痕迹（语义项，归 check 命令）；容量归档由写管道收敛。
"""
import re

DATE_RE = re.compile(r"^- \d{4}-\d{2}-\d{2} ")


def check(ctx):
    issues = []
    for rel, _fm, body in ctx.pages:
        if rel != "log.md" and not (rel.startswith("archive/") and rel.endswith("/log.md")):
            continue
        for i, raw in enumerate(body.splitlines(), 1):
            line = raw.rstrip()
            if line.startswith("- ") and not DATE_RE.match(line):
                issues.append({"级别": "error", "消息": f"{rel}:{i}：条目缺日期（{line[:40]}…）"})
    return issues
