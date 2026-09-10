#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trust 插件附检：机械项（信任字段契约 / stale 清单 / 信任水位）。

stale 页处置分诊（刷新 stale_after、重验证或废弃）是语义项，归 check 命令。
"""
import datetime
import re

ACTOR_RE = re.compile(r"^(human:.+|process:.+|agent/.+)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _bad_actor(val):
    return not ACTOR_RE.match(str(val))


def _bad_date(val):
    s = str(val)
    if not DATE_RE.match(s):
        return True
    try:  # 日历合法性（2026-13-99 这类格式对但非法的日期）
        datetime.date.fromisoformat(s)
        return False
    except ValueError:
        return True


def check(ctx):
    issues = []
    today = datetime.date.today()
    reviewed = confirmed = 0
    for rel, fm, body in ctx.pages:
        gen = fm.get("generated")
        verified = fm.get("verified")
        stale_after = fm.get("stale_after")
        if gen is not None:
            if not isinstance(gen, dict):
                issues.append({"级别": "warning", "消息": f"{rel}：generated 应为块式映射 by/at"})
            elif gen.get("by") is None or gen.get("at") is None:
                issues.append({"级别": "warning", "消息": f"{rel}：generated 缺 by 或 at"})
            else:
                if _bad_actor(gen["by"]):
                    issues.append({"级别": "warning", "消息": f"{rel}：generated.by {gen['by']!r} 不符 actor 约定"})
                if _bad_date(gen["at"]):
                    issues.append({"级别": "warning", "消息": f"{rel}：generated.at {gen['at']!r} 非 YYYY-MM-DD"})
        if verified is not None:
            events = verified if isinstance(verified, list) else [verified]
            has_human = False
            for ev in events:
                text = ev if isinstance(ev, str) else str(ev)
                m_by = re.search(r"by:\s*(.+?)(?:\s*,\s*at:|$)", text)
                m_at = re.search(r"at:\s*(\S+)", text)
                if not m_by or not m_at:
                    issues.append({"级别": "warning", "消息": f"{rel}：verified 事件缺 by 或 at（{text.strip()!r}）"})
                    continue
                by, at = m_by.group(1).strip(), m_at.group(1).rstrip(",");  # 容忍尾逗号
                if _bad_actor(by):
                    issues.append({"级别": "warning", "消息": f"{rel}：verified.by {by!r} 不符 actor 约定"})
                if _bad_date(at):
                    issues.append({"级别": "warning", "消息": f"{rel}：verified.at {at!r} 非 YYYY-MM-DD"})
                if by.startswith("human:"):
                    has_human = True
            if has_human:
                reviewed += 1
            else:
                confirmed += 1
        if stale_after is not None:
            if _bad_date(stale_after):
                issues.append({"级别": "warning", "消息": f"{rel}：stale_after {stale_after!r} 非 YYYY-MM-DD"})
            elif datetime.date.fromisoformat(str(stale_after)) <= today:
                issues.append({"级别": "信息", "消息": f"{rel}：已过 stale_after（{stale_after}）——stale 页，处置归人"})
        if fm.get("sources") is not None and not isinstance(fm.get("sources"), list):
            issues.append({"级别": "warning", "消息": f"{rel}：sources 应为列表"})
    if reviewed or confirmed:
        issues.append({"级别": "信息", "消息": f"信任水位：human-reviewed {reviewed} 页 / machine-confirmed {confirmed} 页（其余 unverified）"})
    return issues
