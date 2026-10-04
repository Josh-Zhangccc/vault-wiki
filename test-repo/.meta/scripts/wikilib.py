#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wiki 页面服务承重件：frontmatter 解析与页面遍历，供附检运行时装配进 ctx。

插件附检脚本不自行 import 本模块——wiki_plugin_kernel.audit 单次扫描 wiki/，
把 (相对路径, frontmatter, 正文) 列表放进 ctx.pages 全体共享（调用节俭）。
与 wiki_plugin_kernel.parse_manifest 同为最小 YAML 子集，但宽松策略不同：
manifest 严格抛错（协议工件），页面 frontmatter 跳过坏行（用户内容不因
格式瑕疵让附检崩溃）。键宽松（非空白非冒号即可）：块映射子键可为目录名、
中文等（structure 声明页实锤需求），顶层协议字段仍为 ASCII。
"""
import os
import re


def _strip_quotes(s):
    return s[1:-1] if len(s) >= 2 and s[0] == '"' and s[-1] == '"' else s


def _strip_comment(s):
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def parse_frontmatter(text):
    """解析 --- 围栏内的最小 YAML 子集；无围栏返回空 dict，坏行跳过。"""
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    data, target = {}, None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            item = _strip_quotes(_strip_comment(raw.strip()[2:]).strip())
            if not isinstance(data.get(target), list):
                data[target] = []
            data[target].append(item)
            continue
        mm = re.match(r"^(\s*)([^:\s][^:]*):\s*(.*)$", raw)
        if not mm:
            continue
        key, val = mm.group(2), _strip_comment(mm.group(3))
        if mm.group(1):
            if not isinstance(data.get(target), dict):
                data[target] = {}
            data[target][key] = _strip_quotes(val)
        else:
            target = key
            if val == "":
                data[key] = None
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                # token 先去空白再去引号：[ai, llm] 第二项带前导空格，不剥离会让词表碎片化
                data[key] = ([_strip_quotes(v.strip()) for v in inner.split(",") if v.strip()]
                             if inner else [])
            else:
                data[key] = _strip_quotes(val)
    return data


def walk_pages(root):
    """遍历 wiki/ 全部 md 页面，产出 (wiki 相对路径, frontmatter dict, 正文 str)。"""
    wiki = os.path.join(root, "wiki")
    for dirpath, dirs, files in os.walk(wiki):
        dirs.sort()
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                text = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                text = open(p, encoding="utf-8", errors="replace").read()
            m = re.match(r"^---\n.*?\n---\n?", text, re.S)
            rel = os.path.relpath(p, wiki).replace(os.sep, "/")
            yield rel, parse_frontmatter(text), (text[m.end():] if m else text)
