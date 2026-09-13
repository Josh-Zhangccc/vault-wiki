#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault 插件附检：镜像 diff、raw_file 悬挂、哈希核验、疑似全文复制、stub 老化。

只读报告——哈希重算等修复动作归命令（actions.md 机械自动项），附检不执行。
参数依据：原库取证（哈希失配 40%、全文复制 33%）与渐进富化承诺（新 stub 免告）。
"""
import datetime
import hashlib
import os
import re

TODAY = datetime.date.today()


def _file_set(root, sub, strip_md):
    """收集子目录文件集（忽略 .gitkeep）；strip_md 时只收 md 并去后缀（代理页集）。"""
    out = set()
    base = os.path.join(root, sub)
    for dirpath, dirs, files in os.walk(base):
        dirs.sort()
        for fn in sorted(files):
            if fn == ".gitkeep":
                continue
            if strip_md and fn == "index.md":
                continue  # 目录索引：导航层保留名（index 插件每目录化），非概念页无对应物
            if strip_md and not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), base).replace(os.sep, "/")
            out.add(rel[:-3] if strip_md else rel)
    return out


def check(ctx):
    issues = []
    root = ctx.root
    real = _file_set(root, "vault", strip_md=False)
    proxy = _file_set(root, os.path.join("wiki", "vault"), strip_md=True)
    for f in sorted(real - proxy):
        issues.append({"level": "info", "message": f"VAULT 待登记（积压）：{f}"})
    for p in sorted(proxy - real):
        issues.append({"level": "error", "message": f"孤儿代理（VAULT 无对应物）：wiki/vault/{p}"})
    for rel, fm, body in ctx.pages:
        if not rel.startswith("vault/"):
            continue
        rf = fm.get("raw_file")
        if not rf:
            continue
        fp = os.path.join(root, rf)
        if not os.path.exists(fp):
            issues.append({"level": "error", "message": f"{rel}：raw_file 指向不存在（{rf}）"})
            continue
        sh = fm.get("raw_sha256")
        if sh and hashlib.sha256(open(fp, "rb").read()).hexdigest() != sh:
            issues.append({"level": "warning", "message": f"{rel}：raw_sha256 失配（原文已变；描述仍适用则机械重算）"})
        if rf.endswith(".md"):
            try:
                raw_text = open(fp, encoding="utf-8").read()
            except UnicodeDecodeError:
                raw_text = open(fp, encoding="utf-8", errors="replace").read()
            if raw_text and len(body) >= 0.8 * len(raw_text):
                issues.append({"level": "warning", "message": f"{rel}：疑似全文复制（正文 ≥80% 原文；日记类豁免为语义判断）"})
        if not body.strip():  # stub：正文无一行描述
            m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(fm.get("updated") or ""))
            if m:
                age = (TODAY - datetime.date(*map(int, m.groups()))).days
                if age > 90:
                    issues.append({"level": "warning", "message": f"{rel}：stub 超 90 天无描述（新 stub 免告）"})
    return issues
