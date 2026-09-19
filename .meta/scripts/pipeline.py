#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派生层写后管道：index / tags / hot / log / verify。

定位（.meta/protocol/actions.md 执行原则）：确定性的结构操作交给本脚本，
语义判断交给 LLM。重建与滚动规则、窗口参数以本文件源码为准（脚本源码即
规则清单），PLUGIN.md 保留语义说明；命令收尾统一引用本管道，不各自手写
派生页。verify 是写后自证（attester 最小形）：LLM 执行、脚本认证。

用法:
  python .meta/scripts/pipeline.py index              # 重建索引（溢出减负制，幂等；含并回后的多余索引删除）
  python .meta/scripts/pipeline.py tags               # 重建 wiki/tags.md（幂等）
  python .meta/scripts/pipeline.py hot <类型> <一句话>   # 淘汰越界 + 置顶加热缓存条目
  python .meta/scripts/pipeline.py log <类型> <一句话>   # 容量归档 + 置顶加 log 行
  python .meta/scripts/pipeline.py verify             # 写后自证：附检 + 派生区漂移检查

类型枚举：map / save / query / check / plugin / other（log 插件）。
概念页判定（谁入索引）：wiki/ 下所有 .md，排除——保留名（index.md、log.md）、
wiki 根派生页（hot.md、tags.md）、archive/ 子树（不可变区，本脚本永不改写其中文件）、
tmp/ 子树（临时区：派生层隐身，无留存承诺，见 tmp 插件）。
索引溢出减负制：单张索引清单 ≤INDEX_MAX_ENTRIES 条（页条目 + 目录条目）；根索引恒在，
超窗时按子树页数降序（同数按名序）切出子目录自立索引，直至装下；纯函数重建（同结构同结果）。
"""
import datetime
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikilib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = os.path.join(ROOT, "wiki")
FORMAT_VERSION = "0.2"
DESC_MAX = 80
ROOT_RESERVED = {"hot.md", "tags.md"}  # wiki 根派生页（log.md/index.md 为保留名，统一排除）

# 滚动窗口参数（hot / log 插件的机械权威源；PLUGIN.md 为语义说明）
HOT_MAX_ENTRIES = 25
HOT_MAX_DAYS = 5
HOT_MAX_CHARS = 200
LOG_MAX_ENTRIES = 100
INDEX_MAX_ENTRIES = 25  # 单张索引清单窗口（页条目 + 目录条目；溢出减负切分依据）
TYPE_ORDER = ["map", "save", "query", "check", "plugin", "other"]
HOT_HEADER = ("# 热缓存\n\n> 最近变更摘要；≤25 条且 <5 日，窗外即删；可整体再生。"
              "规则见 `.meta/plugins/hot/`，写走 `pipeline.py hot`。\n")
LOG_HEADER = ("# 运行日志\n\n> 置顶追加、只增不删；条目 = `- YYYY-MM-DD <类型>：一句话`。"
              "规则见 `.meta/plugins/log/`，写走 `pipeline.py log`。\n")
DATE_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) ")


def _today():
    return datetime.date.today().isoformat()


# ---------- 概念页与 index / tags ----------

def _cut(text):
    return text if len(text) <= DESC_MAX else text[: DESC_MAX - 1] + "…"


def _desc(fm, body):
    d = fm.get("description")
    if d:
        return _cut(str(d))
    for line in body.splitlines():
        t = line.strip()
        if t and not t.startswith(("#", ">", "|", "```")):
            return _cut(t)
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
        if rel.startswith("tmp/") or d.startswith("tmp/") or d == "tmp":
            continue  # 临时区：派生层隐身
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
        if "tmp" in subdirs:
            subdirs.remove("tmp")  # 临时区不建索引
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


def plan_index_dirs(pages, dirs):
    """溢出减负规划：返回应生成 index.md 的目录集（根恒在）。

    目录清单 = 本目录概念页 + 未切子树页（透明内联）+ 目录条目行；超窗时按
    子树页数降序（同数按名序）切出子目录自立索引，直至装下。切出至少省
    S-1 行，故 S<2 的子目录永不被切；空子树（S=0）内联成本按 1 行计（可见性行）。
    纯函数：同结构必同结果，无历史状态。
    """
    own = {}
    for _, d, _, _ in pages:
        own[d] = own.get(d, 0) + 1

    planned = set()

    def plan(d):
        planned.add(d)
        kids = subdirs_of(d, dirs)
        sizes = {c: _count_subtree((d + "/" + c) if d else c, pages) for c in kids}
        total = own.get(d, 0) + sum(s if s > 0 else 1 for s in sizes.values())
        if total <= INDEX_MAX_ENTRIES:
            return
        for c in sorted((k for k in kids if sizes[k] >= 2),
                        key=lambda c: (-sizes[c], c)):
            if total <= INDEX_MAX_ENTRIES:
                break
            plan((d + "/" + c) if d else c)
            total -= sizes[c] - 1

    plan("")
    return planned


def visible_pages(d, pages, planned):
    """d 的索引直列页面：本目录页 + 途经无已切目录的全部下级页（透明内联）。"""
    pre = d + "/" if d else ""
    out = []
    for name, dd, fm, desc in pages:
        if dd == d:
            out.append((name, fm, desc))
        elif dd.startswith(pre):
            parts = dd[len(pre):].split("/")
            if all((pre + "/".join(parts[:i])) not in planned for i in range(1, len(parts) + 1)):
                out.append((name, fm, desc))
    return out


def render_index(d, pages, dirs, planned):
    """目录 d 的 index.md 全文（溢出减负制：直列可达页，已切子目录作入口行）。"""
    is_root = d == ""
    lines = []
    if is_root:
        lines += ["---", f"format_version: {FORMAT_VERSION}", "---", ""]
    lines.append("# 索引" if is_root else f"# {d.rsplit('/', 1)[-1]} 索引")
    lines.append("")
    tip = ("溢出减负：本页直列可达页面；清单超窗时子目录自立索引（入口行带页数），下钻读之。"
           if is_root else "本目录索引：直列未切子树页面，已切子目录见入口行。")
    lines.append(f"> {tip}只聚合、永不手编，由 index 插件经 `pipeline.py index` 重建。")
    lines.append("")
    entries = []
    for s in subdirs_of(d, dirs):
        full = (d + "/" + s) if d else s
        n = _count_subtree(full, pages)
        if full in planned:
            entries.append(f"- [[{full}/index|{s}/]]（{n} 页）")
        elif n == 0:
            entries.append(f"- {s}/（0 页）")  # 空子树可见性行：无索引可链，不入断链图
    if entries:
        lines += ["## 子目录", ""] + entries + [""]
    groups = {}
    for name, fm, desc in visible_pages(d, pages, planned):
        groups.setdefault(str(fm.get("type") or "未分类"), []).append((name, desc))
    for t in sorted(groups):
        lines.append(f"## {t}")
        lines.append("")
        for name, desc in sorted(groups[t]):
            lines.append(f"- [[{name}]] —— {desc}")
        lines.append("")
    if not entries and not groups:
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


def index_targets():
    pages = concept_pages()
    dirs = all_dirs(pages)
    planned = plan_index_dirs(pages, dirs)
    targets = {(d + "/" if d else "") + "index.md": render_index(d, pages, dirs, planned)
               for d in planned}
    return planned, targets


def write_changed(path, content):
    if os.path.exists(path) and open(path, encoding="utf-8").read() == content:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(content)
    return True


def do_index(check_only=False):
    _, targets = index_targets()
    drift, changed = [], 0
    for rel, content in sorted(targets.items()):
        path = os.path.join(WIKI, rel)
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if cur == content:
            continue
        if check_only:
            drift.append(rel)
        elif write_changed(path, content):
            changed += 1
            print(f"[index] rebuilt wiki/{rel}")
    # 非计划 index.md（减负并回后的旧索引）：删除 / 报漂移；archive/ 与 tmp/ 子树不碰
    for dirpath, subdirs, files in os.walk(WIKI):
        if "archive" in subdirs:
            subdirs.remove("archive")  # 不下钻不可变区
        if "tmp" in subdirs:
            subdirs.remove("tmp")  # 临时区非本管道辖域
        if "index.md" not in files:
            continue
        rel = os.path.relpath(os.path.join(dirpath, "index.md"), WIKI).replace(os.sep, "/")
        if rel not in targets:
            if check_only:
                drift.append(rel)
            else:
                os.remove(os.path.join(WIKI, rel))
                changed += 1
                print(f"[index] removed wiki/{rel}（并回上级）")
    if not check_only:
        print(f"[index] done, {changed} file(s) changed (idempotent)")
    return drift


def do_tags(check_only=False):
    path = os.path.join(WIKI, "tags.md")
    content = render_tags(concept_pages())
    cur = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if cur == content:
        if not check_only:
            print("[tags] unchanged")
        return []
    if check_only:
        return ["tags.md"]
    write_changed(path, content)
    print("[tags] rebuilt wiki/tags.md")
    return []


# ---------- hot / log 滚动 ----------

def do_hot(kind, text):
    if kind not in TYPE_ORDER:
        print(f"[hot] type must be one of {'/'.join(TYPE_ORDER)} (got {kind})")
        return False
    entry = f"- {_today()} {text}"[:HOT_MAX_CHARS]
    # 收集既有条目（带节归属），机械淘汰越界
    sections = {t: [] for t in TYPE_ORDER}
    hot_path = os.path.join(WIKI, "hot.md")
    if os.path.exists(hot_path):
        cur = None
        for raw in open(hot_path, encoding="utf-8").read().splitlines():
            m = re.match(r"^##\s*Recent (\S+)", raw)
            if m and m.group(1) in TYPE_ORDER:
                cur = m.group(1)
                continue
            dm = DATE_RE.match(raw)
            if dm and cur:
                if (datetime.date.today() - datetime.date.fromisoformat(dm.group(1))).days < HOT_MAX_DAYS:
                    sections[cur].append(raw[:HOT_MAX_CHARS])
    sections[kind].insert(0, entry)  # 置顶
    flat = [e for t in TYPE_ORDER for e in sections[t]]
    if len(flat) > HOT_MAX_ENTRIES:  # 整体超限：按日期统一取新近 25 条（稳定排序，同日保持节序）
        keep = set(sorted(flat, key=lambda e: e[2:12], reverse=True)[:HOT_MAX_ENTRIES])
        for t in TYPE_ORDER:
            sections[t] = [e for e in sections[t] if e in keep]
    body = [HOT_HEADER.rstrip()]
    any_entry = False
    for t in TYPE_ORDER:
        if not sections[t]:
            continue
        any_entry = True
        body += ["", f"## Recent {t}", ""] + sections[t]
    if not any_entry:
        body += ["", "（暂无）"]
    write_changed(hot_path, "\n".join(body) + "\n")
    print(f"[hot] written ({kind}), {min(len(flat), HOT_MAX_ENTRIES)} entries")
    return True


def do_log(kind, text):
    if kind not in TYPE_ORDER:
        print(f"[log] type must be one of {'/'.join(TYPE_ORDER)} (got {kind})")
        return False
    log_path = os.path.join(WIKI, "log.md")
    entries = []
    if os.path.exists(log_path):
        for raw in open(log_path, encoding="utf-8").read().splitlines():
            if DATE_RE.match(raw):
                entries.append(raw)
    entries.insert(0, f"- {_today()} {kind}：{text}")  # 置顶追加，既有条目不改写
    overflow = entries[LOG_MAX_ENTRIES:]
    if overflow:  # 窗口超限：最旧一段按条目月份分组搬入 archive/<月>/log.md（只搬位置）
        for month in sorted({e[2:9] for e in overflow}):
            moved = [e for e in overflow if e[2:9] == month]
            adir = os.path.join(WIKI, "archive", month)
            apath = os.path.join(adir, "log.md")
            old = open(apath, encoding="utf-8").read() if os.path.exists(apath) else f"# 归档 {month}\n"
            write_changed(apath, old.rstrip() + "\n" + "\n".join(moved) + "\n")
            print(f"[log] archived {len(moved)} entries to wiki/archive/{month}/log.md")
    write_changed(log_path, LOG_HEADER + "\n" + "\n".join(entries[:LOG_MAX_ENTRIES]) + "\n")
    print(f"[log] written ({kind}), main file {min(len(entries), LOG_MAX_ENTRIES)} entries")
    return True


# ---------- 写后自证 ----------

def do_verify():
    ok = True
    r = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki_plugin_kernel.py"), "audit"])
    if r.returncode != 0:
        ok = False
        print("[verify] plugin audit has errors")
    drift = do_index(check_only=True) + do_tags(check_only=True)
    if drift:
        ok = False
        print("[verify] derived drift: " + ", ".join("wiki/" + d for d in drift) + " (run pipeline.py index / tags to fix)")
    else:
        print("[verify] derived area consistent")
    print("[verify] " + ("passed" if ok else "failed"))
    return 0 if ok else 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "index":
        do_index()
        return 0
    if cmd == "tags":
        do_tags()
        return 0
    if cmd == "hot":
        return 0 if do_hot(sys.argv[2], " ".join(sys.argv[3:])) else 1
    if cmd == "log":
        return 0 if do_log(sys.argv[2], " ".join(sys.argv[3:])) else 1
    if cmd == "verify":
        return do_verify()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
