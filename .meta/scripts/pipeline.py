#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派生层写后管道：index / tags 的确定性重建。

定位（.meta/protocol/actions.md 执行原则）：确定性的结构操作交给本脚本，
语义判断交给 LLM。重建规则与参数以本文件源码为准（脚本源码即规则清单），
PLUGIN.md 保留语义说明；命令收尾统一引用本管道，不各自手写派生页。

用法:
  python .meta/scripts/pipeline.py index   # 重建全部目录 index.md（幂等，只写有变化的文件）
  python .meta/scripts/pipeline.py tags    # 重建 wiki/tags.md（幂等）

概念页判定（谁入索引）：wiki/ 下所有 .md，排除——
  - 保留名文件：任何目录下的 index.md、log.md（OKF 对齐：保留名非概念页）
  - wiki 根的派生页：hot.md、tags.md
  - archive/ 子树（不可变区，本脚本永不生成/改写其中的文件）
索引条目描述：frontmatter description 优先，否则正文首个非空非结构行截 80 字。
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikilib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = os.path.join(ROOT, "wiki")
OKF_VERSION = "0.2"
DESC_MAX = 80
ROOT_RESERVED = {"hot.md", "tags.md"}  # wiki 根派生页（log.md/index.md 为保留名，统一排除）


def _desc(fm, body):
    d = fm.get("description")
    if d:
        return str(d)[:DESC_MAX]
    for line in body.splitlines():
        t = line.strip()
        if t and not t.startswith(("#", ">", "|", "```")):
            return t[:DESC_MAX]
    return "（无描述）"


def concept_pages():
    """[(页面全名=路径去 .md, 所在目录, frontmatter, 描述)]，按全名排序。"""
    out = []
    for rel, fm, body in wikilib.walk_pages(ROOT):
        d, _, fn = rel.rpartition("/")
        if fn in ("index.md", "log.md"):
            continue  # 保留名：非概念页
        if d == "" and fn in ROOT_RESERVED:
            continue
        if rel.startswith("archive/") or d.startswith("archive/") or d == "archive":
            continue
        out.append((rel[:-3], d, fm, _desc(fm, body)))
    return sorted(out)


def all_dirs(pages):
    """wiki/ 下应生成 index 的目录集（含空目录；排除 archive/ 子树）。"""
    dirs = {""}
    for _, d, _, _ in pages:
        parts = d.split("/") if d else []
        for i in range(len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    for dirpath, subdirs, _files in os.walk(WIKI):
        if "archive" in subdirs:
            subdirs.remove("archive")  # 不下钻不可变区
        rel = os.path.relpath(dirpath, WIKI).replace(os.sep, "/")
        dirs.add("" if rel == "." else rel)
    return dirs


def subdirs_of(d, dirs):
    """d 的直接子目录名（已排序）。"""
    prefix = d + "/" if d else ""
    depth = d.count("/") + 1 if d else 0
    return sorted(x[len(prefix):] for x in dirs
                  if x != d and x.startswith(prefix) and x.count("/") == depth)


def _count_subtree(full, pages):
    return sum(1 for name, d, _, _ in pages if d == full or d.startswith(full + "/"))


def render_index(d, pages, dirs):
    """目录 d 的 index.md 全文。pages 为全库概念页（供子目录计数）。"""
    is_root = d == ""
    lines = []
    if is_root:
        lines += ["---", f"okf_version: {OKF_VERSION}", "---", ""]
    lines.append("# 索引" if is_root else f"# {d.rsplit('/', 1)[-1]} 索引")
    lines.append("")
    tip = ("每目录一份（渐进披露）：本页只列顶层概念与子目录入口，下钻读各目录 index。"
           if is_root else "本目录清单；下钻读子目录 index。")
    lines.append(f"> {tip}只聚合、永不手编，由 index 插件经 `pipeline.py index` 重建。")
    lines.append("")
    subs = subdirs_of(d, dirs)
    own = [(name, fm, desc) for name, dd, fm, desc in pages if dd == d]
    if subs:
        lines.append("## 子目录")
        lines.append("")
        for s in subs:
            full = (d + "/" + s) if d else s
            lines.append(f"- [[{full}/index|{s}/]]（{_count_subtree(full, pages)} 页）")
        lines.append("")
    groups = {}
    for name, fm, desc in own:
        groups.setdefault(str(fm.get("type") or "未分类"), []).append((name, desc))
    for t in sorted(groups):
        lines.append(f"## {t}")
        lines.append("")
        for name, desc in sorted(groups[t]):
            lines.append(f"- [[{name}]] —— {desc}")
        lines.append("")
    if not subs and not groups:
        lines.append("（暂无页面）")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tags(pages):
    tag_map = {}
    for name, d, fm, _ in pages:
        tags = fm.get("tags")
        if tags is None:
            continue
        if not isinstance(tags, list):
            tags = [tags]
        for t in tags:
            tag_map.setdefault(str(t), []).append(name)
    lines = ["# tag 索引", "",
             "> tag → 页面反向索引；只聚合、永不手编，由 index 插件经 `pipeline.py tags` 重建。", ""]
    if not tag_map:
        lines.append("（暂无）")
        lines.append("")
    for t in sorted(tag_map):
        lines.append(f"## {t}")
        lines.append("")
        for name in sorted(tag_map[t]):
            lines.append(f"- [[{name}]]")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_changed(path, content):
    if os.path.exists(path) and open(path, encoding="utf-8").read() == content:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(content)
    return True


def do_index():
    pages = concept_pages()
    dirs = all_dirs(pages)
    changed = 0
    for d in sorted(dirs):
        path = os.path.join(WIKI, d, "index.md") if d else os.path.join(WIKI, "index.md")
        if write_changed(path, render_index(d, pages, dirs)):
            changed += 1
            print(f"[索引] 已重建 wiki/{d + '/' if d else ''}index.md")
    print(f"[索引] 完成：{len(dirs)} 个目录，{changed} 个文件有变化（幂等）")
    return True


def do_tags():
    if write_changed(os.path.join(WIKI, "tags.md"), render_tags(concept_pages())):
        print("[tags] 已重建 wiki/tags.md")
    else:
        print("[tags] 一致，无变化")
    return True


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "index":
        return 0 if do_index() else 1
    if cmd == "tags":
        return 0 if do_tags() else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
