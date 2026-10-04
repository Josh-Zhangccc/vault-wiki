#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""device 插件附检：设备档案页 warranty_until 临期与过期扫描。

临期窗口 30 天（写死，边用边改）；处置经确认走 todo，本脚本只报告。
"""
from datetime import date


def check(ctx):
    issues = []
    today = date.today()
    for rel, fm, _body in ctx.pages:
        dev = fm.get("device")
        if not dev or not isinstance(dev, dict):
            continue
        wu = str(dev.get("warranty_until") or "").strip()
        if not wu:
            continue
        try:
            due = date.fromisoformat(wu)
        except ValueError:
            issues.append({"level": "warning", "message": f"{rel}：warranty_until 非法日期：{wu}"})
            continue
        if due < today:
            issues.append({"level": "warning", "message": f"{rel}：保修/保障已过期 {wu}（处置经确认入 todo）"})
        elif (due - today).days <= 30:
            issues.append({"level": "warning", "message": f"{rel}：保修/保障临期 {wu}（≤30 天，处置经确认入 todo）"})
    return issues
