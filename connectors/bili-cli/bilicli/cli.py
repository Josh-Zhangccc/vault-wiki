"""bili-cli 命令面：argparse 子命令，输出恒单行 JSON。

读 = 查询即答（蒸馏字段，非全量透传）；写 = 低危白名单（watchlater/fav/like），
全部须 --yes 显式门——agent 层另有「用户明示动词」纪律，双层防误触。
"""

import argparse
import json
import sys
import time

from . import __version__, auth
from .api import BiliAPI


def _emit(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def _ts(v):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(v)) if v else None


def _need_yes(args, action: str) -> None:
    if not getattr(args, "yes", False):
        print(f"写操作 {action} 须 --yes（agent 层另须用户明示动词）", file=sys.stderr)
        raise SystemExit(2)


def cmd_login(args):
    jar = auth.parse_cookie_string(args.file.read_text(encoding="utf-8")) if args.file \
        else auth.parse_cookie_string(args.cookie)
    auth.save_cookies(jar)
    api = BiliAPI()
    me = api.me() or {}
    _emit({"ok": True, "mid": me.get("mid"), "uname": me.get("uname"),
           "is_login": me.get("isLogin"), "stored": str(auth.COOKIE_FILE)})


def cmd_me(args):
    api = BiliAPI(); api.require_auth("me")
    d = api.me() or {}
    vip = d.get("vip") or {}
    _emit({
        "mid": d.get("mid"), "uname": d.get("uname"),
        "level": (d.get("level_info") or {}).get("current_level"),
        "coins": d.get("coins"),
        "vip": {"status": vip.get("status"), "due": _ts(vip.get("due_date"))},
        "following": d.get("following"), "follower": d.get("follower"),
    })


def cmd_watchlater(args):
    api = BiliAPI(); api.require_auth("watchlater")
    if args.action == "list":
        rows = (api.watchlater() or {}).get("list") or []
        _emit([{
            "bvid": r.get("bvid"), "title": r.get("title"),
            "owner": r.get("owner", {}).get("name"),
            "added_at": _ts(r.get("add_at")), "duration_s": r.get("duration"),
        } for r in rows])
        return
    _need_yes(args, args.action)
    fn = {"add": api.watchlater_add, "remove": api.watchlater_del}[args.action]
    _emit({**fn(args.bvid), "action": f"watchlater {args.action}", "bvid": args.bvid})


def cmd_fav(args):
    api = BiliAPI(); api.require_auth("fav")
    if not args.action or args.action == "list":
        if args.fid:
            rows = api.fav_list(args.fid, args.limit) or []
            _emit([{
                "bvid": r.get("bvid"), "title": r.get("title"),
                "upper": (r.get("upper") or {}).get("name"),
                "duration_s": r.get("duration"), "fav_time": _ts(r.get("fav_time")),
            } for r in rows])
        else:
            rows = api.fav_folders() or []
            _emit([{
                "fid": r.get("id"), "title": r.get("title"),
                "count": r.get("media_count"), "fav_time": _ts(r.get("fav_time")),
            } for r in rows])
        return
    _need_yes(args, args.action)
    if args.action == "move":
        if not (args.src_fid and args.dst_fid):
            raise SystemExit("fav move 须 --from <源夹id> --to <目标夹id>（先 `bili-cli fav` 查清单）")
        _emit({**api.fav_move(args.bvid, args.src_fid, args.dst_fid), "action": "fav move",
               "bvid": args.bvid, "from": args.src_fid, "to": args.dst_fid})
        return
    if not args.fid:
        raise SystemExit("--fid 必带（收藏夹 id，先 `bili-cli fav` 查清单）")
    fn = {"add": api.fav_add, "remove": api.fav_del}[args.action]
    _emit({**fn(args.bvid, args.fid), "action": f"fav {args.action}",
           "bvid": args.bvid, "fid": args.fid})


def cmd_history(args):
    api = BiliAPI(); api.require_auth("history")
    rows = api.history(args.limit)
    _emit([{
        "bvid": r.get("bvid"), "title": r.get("title"),
        "owner": (r.get("owner") or {}).get("name"),
        "progress_s": r.get("progress"), "duration_s": r.get("duration"),
        "view_at": _ts(r.get("view_at")),
    } for r in rows])


def cmd_search(args):
    import re
    clean = lambda t: re.sub(r"<[^>]+>", "", t or "")  # 剥搜索高亮 <em> 标签
    rows = BiliAPI().search(args.query, args.kind, args.limit)
    if args.kind == "up":
        _emit([{
            "mid": r.get("mid"), "name": clean(r.get("uname")), "fans": r.get("fans"),
            "sign": clean(r.get("usign")), "videos": r.get("videos"),
        } for r in rows])
    else:
        _emit([{
            "bvid": r.get("bvid"), "title": clean(r.get("title")),
            "author": clean(r.get("author")), "play": r.get("play"),
            "duration": r.get("duration"), "pubdate": _ts(r.get("pubdate")),
        } for r in rows])


def cmd_video(args):
    d = BiliAPI().video(args.bvid) or {}
    stat, pages = d.get("stat") or {}, d.get("pages") or []
    _emit({
        "bvid": d.get("bvid"), "aid": d.get("aid"), "title": d.get("title"),
        "owner": {"mid": (d.get("owner") or {}).get("mid"),
                  "name": (d.get("owner") or {}).get("name")},
        "pubdate": _ts(d.get("pubdate")), "duration_s": d.get("duration"),
        "stat": {k: stat.get(k) for k in ("view", "danmaku", "reply", "favorite", "coin", "like")},
        "pages": [{"page": p.get("page"), "part": p.get("part"), "cid": p.get("cid"),
                   "duration_s": p.get("duration")} for p in pages],
        "desc_head": (d.get("desc") or "")[:200],
    })


def cmd_subtitle(args):
    _emit(BiliAPI().subtitle(args.bvid, args.page, ai=args.ai))


def cmd_summary(args):
    api = BiliAPI(); api.require_auth("summary")  # 实测 -101：官方总结仅登录态开放
    _emit(api.summary(args.bvid))


def cmd_up(args):
    api = BiliAPI()
    d = api.up_info(args.mid) or {}
    out = {
        "mid": d.get("mid"), "name": d.get("name"), "sign": d.get("sign"),
        "fans": d.get("follower"), "videos": d.get("archive_count"),
        "joined": _ts(d.get("jointime")),
    }
    if args.arcs:
        out["arcs"] = [{
            "bvid": v.get("bvid"), "title": v.get("title"),
            "created": _ts(v.get("created")), "play": v.get("play"),
        } for v in api.up_arcs(args.mid, args.limit)]
    _emit(out)


def cmd_like(args):
    _need_yes(args, "like")
    api = BiliAPI(); api.require_auth("like")
    _emit({**api.like(args.bvid), "action": "like", "bvid": args.bvid})


def cmd_raw(args):
    _emit(BiliAPI().raw(args.url, post=args.post))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bili-cli",
                                description="bilibili 只读为主连接器（web cookie；写命令须 --yes）")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login", help="导入浏览器 cookie（SESSDATA/bili_jct）")
    s.add_argument("--cookie", help='cookie 串，如 "SESSDATA=..; bili_jct=..; buvid3=.."')
    s.add_argument("--file", type=argparse.FileType("r", encoding="utf-8"),
                   help="或自文件读同格式串")
    s.set_defaults(fn=cmd_login)

    s = sub.add_parser("me", help="我的信息（mid/昵称/等级/VIP）")
    s.set_defaults(fn=cmd_me)

    s = sub.add_parser("watchlater", help="稍后再看（读 / 增删写）")
    s.add_argument("action", nargs="?", choices=["list", "add", "remove"], default="list")
    s.add_argument("bvid", nargs="?", help="写操作目标（如 BV1xx411c7mD）")
    s.add_argument("--yes", action="store_true", help="写操作显式确认门")
    s.set_defaults(fn=cmd_watchlater)

    s = sub.add_parser("fav", help="收藏夹（夹清单/内容读 / 增删移写）")
    s.add_argument("action", nargs="?", choices=["list", "add", "remove", "move"], default="list")
    s.add_argument("bvid", nargs="?", help="写操作目标")
    s.add_argument("--fid", type=int, help="收藏夹 id（读内容/写操作均需）")
    s.add_argument("--from", dest="src_fid", type=int, help="move 源夹 id")
    s.add_argument("--to", dest="dst_fid", type=int, help="move 目标夹 id")
    s.add_argument("--limit", type=int, default=30)
    s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_fav)

    s = sub.add_parser("history", help="观看历史（近窗）")
    s.add_argument("--limit", type=int, default=30)
    s.set_defaults(fn=cmd_history)

    s = sub.add_parser("search", help="搜索（视频 / UP 主）")
    s.add_argument("query")
    s.add_argument("--kind", choices=["video", "up"], default="video")
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("video", help="视频详情（分P/统计/简介）")
    s.add_argument("bvid")
    s.set_defaults(fn=cmd_video)

    s = sub.add_parser("subtitle", help="字幕正文（默认 CC 轨道，--ai 强制 AI 轨道）")
    s.add_argument("bvid")
    s.add_argument("--page", type=int, default=1, help="分P 序号")
    s.add_argument("--ai", action="store_true", help="取 AI 字幕轨道（lan ai-*）")
    s.set_defaults(fn=cmd_subtitle)

    s = sub.add_parser("summary", help="官方 AI 视频总结（无则 has_summary=false，走降级链）")
    s.add_argument("bvid")
    s.set_defaults(fn=cmd_summary)

    s = sub.add_parser("up", help="UP 主信息（可带投稿列表）")
    s.add_argument("mid", type=int)
    s.add_argument("--arcs", action="store_true", help="带最新投稿")
    s.add_argument("--limit", type=int, default=20, help="投稿条数（--arcs 时）")
    s.set_defaults(fn=cmd_up)

    s = sub.add_parser("like", help="点赞视频（写，须 --yes）")
    s.add_argument("bvid")
    s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_like)

    s = sub.add_parser("raw", help="任意端点透传（GET/POST JSON）")
    s.add_argument("url")
    s.add_argument("--post", action="store_true")
    s.set_defaults(fn=cmd_raw)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    args.fn(args)
    return 0
