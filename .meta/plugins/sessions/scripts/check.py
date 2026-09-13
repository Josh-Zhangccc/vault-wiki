#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sessions 插件附检：机械项（领地边界 / participants 契约）。

骨干页是否该提升未提升是语义项（膨胀判断），归 check 命令。
"""
import re

ACTOR_RE = re.compile(r"^(human:.+|process:.+|agent/.+)$")


def check(ctx):
    issues = []
    for rel, fm, body in ctx.pages:
        if rel.endswith("/index.md") or rel == "index.md":
            continue  # 派生页非骨干页，不参与领地判定
        ptype = fm.get("type")
        in_sessions = rel.startswith("sessions/")
        if ptype == "session" and not in_sessions:
            issues.append({"level": "warning", "message": f"{rel}：session 型页面应在 wiki/sessions/（sessions 插件领地）"})
        elif in_sessions and ptype != "session":
            issues.append({"level": "warning", "message": f"{rel}：wiki/sessions/ 内页面应为 type: session（实为 {ptype or '未标'}）"})
        if ptype == "session" or in_sessions:
            parts = fm.get("participants")
            if parts is None:
                issues.append({"level": "warning", "message": f"{rel}：缺 participants（actor 列表）"})
            else:
                if not isinstance(parts, list):
                    parts = [parts]
                for p in parts:
                    if not ACTOR_RE.match(str(p)):
                        issues.append({"level": "warning", "message": f"{rel}：participants 项 {p!r} 不符 actor 约定（human:名 / process:名 / agent/模型）"})
    return issues
