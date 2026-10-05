"""bilibili web API 薄封装：session（cookie/buvid/UA/Referer）、WBI 签名、端点方法。

只读为主；写方法仅限连接器纪律放行的低危白名单（稍后再看/收藏/点赞），
调用方（cli.py）负责 --yes 门与 csrf 注入。
"""

import time
from hashlib import md5
from urllib.parse import urlencode

import requests

from . import auth
from .config import API_BASE, APP_URL, ENDPOINTS, USER_AGENT

# WBI mixin key 重排表（社区稳定公开值，2023 起启用；随 nav 下发密钥轮换，表本身不变）
_MIXIN_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52,
]


class BiliAPI:
    def __init__(self, authed: bool = True):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT, "Referer": APP_URL + "/"})
        self.s.params = {}
        self.csrf = ""
        self.authed = False
        if authed:
            try:
                jar = auth.load_cookies()
            except SystemExit:
                jar = None  # 无凭据文件 → 匿名（search/video/up 等公开端点仍可用）
            if jar:
                self.s.cookies.update(jar)
                self.csrf = jar.get("bili_jct", "")
                self.authed = True
        # buvid3 是风控基础面，匿名（search 等 WBI 端点）同样需要
        self._ensure_buvid()
        self._wbi_key = None

    def require_auth(self, cmd: str) -> None:
        """个人数据与写命令的登录门槛；公开查询（search/video/up/subtitle）不设。"""
        if not self.authed:
            raise SystemExit(
                f"{cmd} 需登录态：先 bili-cli login --cookie '...'（凭据只存 ~/.bili-cli/）")

    # -- 基础件 ---------------------------------------------------------

    def _ensure_buvid(self):
        if self.s.cookies.get("buvid3"):
            return
        r = self.s.get(API_BASE + ENDPOINTS["spi"][0], timeout=15)
        for k in ("b_3", "b_4"):
            v = (r.json().get("data") or {}).get(k)
            if v:
                self.s.cookies.set({"b_3": "buvid3", "b_4": "buvid4"}[k], v)

    def _wbi_mixin_key(self) -> str:
        if self._wbi_key is None:
            nav = self.s.get(API_BASE + ENDPOINTS["nav"][0], timeout=15).json()
            wbi = nav.get("data", {}).get("wbi_img") or {}
            img = wbi.get("img_url", "").rsplit("/", 1)[-1].split(".")[0]
            sub = wbi.get("sub_url", "").rsplit("/", 1)[-1].split(".")[0]
            raw = img + sub
            self._wbi_key = "".join(raw[i] for i in _MIXIN_TAB[:32])
        return self._wbi_key

    def _sign(self, params: dict) -> dict:
        params = {k: str(v) for k, v in params.items()}
        params["wts"] = int(time.time())
        qs = urlencode(sorted(params.items(), key=lambda kv: kv[0]))
        for ch in "!'()*":
            qs = qs.replace(ch, "")
            # 注：过滤针对 value；此处整体替换足够（这些字符在键中不出现，值中出现即被剥离，与站方行为一致）
        params["w_rid"] = md5((qs + self._wbi_mixin_key()).encode()).hexdigest()
        return params

    def _call(self, name: str, params: dict | None = None, post: bool = False,
              extra_form: dict | None = None, headers: dict | None = None):
        path, need_wbi = ENDPOINTS[name]
        params = dict(params or {})
        if post:
            form = {**params, **(extra_form or {})}
            if self.csrf:
                form.setdefault("csrf", self.csrf)
                form.setdefault("csrf_token", self.csrf)
            r = self.s.post(API_BASE + path, data=form, timeout=15)
        else:
            if need_wbi:
                params = self._sign(params)
            r = self.s.get(API_BASE + path, params=params, timeout=15, headers=headers)
        try:
            body = r.json()
        except ValueError:
            raise SystemExit(f"非 JSON 响应（HTTP {r.status_code}）——端点可能改版，用 raw 透传核对")
        if body.get("code") != 0:
            raise SystemExit(f"API 错误 code={body.get('code')}: {body.get('message')}")
        return body.get("data")

    # space 系端点（up_info/up_arc）风控最严：需 space 页 Referer + 浏览器指纹参数，
    # 否则 -352；指纹值取社区通行静态串（与真实指纹无关，仅满足校验存在性）
    _DM_PARAMS = {
        "dm_img_list": "[]",
        "dm_img_str": "V2ViR0wgMS4wIChXaW5kb3dzKQ==",
        "dm_cover_img_str": "QU5HTEUgKEFNUCwgQU1QIEFNUCBTSEExKSBEaXJlY3QzRDExX3ZzXzVfMCBl",
        "dm_img_inter": '{"ds":[],"wh":[0,0,0,0],"of":[0,0,0,0]}',
    }

    def _space_headers(self, mid: int) -> dict:
        return {"Referer": f"https://space.bilibili.com/{mid}/"}

    # -- 读（查询即答） ---------------------------------------------------

    def me(self):
        return self.s.get(API_BASE + ENDPOINTS["nav"][0], timeout=15).json().get("data")

    def watchlater(self):
        return self._call("watchlater")

    def history(self, limit: int = 30):
        out, max_cursor = [], 0
        while len(out) < limit:
            data = self._call("history", {"ps": min(30, limit - len(out)), "max": max_cursor})
            rows = (data or {}).get("list") or []
            if not rows:
                break
            out.extend(rows)
            max_cursor = rows[-1]["view_at"]
        return out[:limit]

    def fav_folders(self):
        return (self._call("fav_folders") or {}).get("list")

    def fav_list(self, fid: int, limit: int = 30):
        data = self._call("fav_list", {
            "media_id": fid, "pn": 1, "ps": min(20 * ((limit + 19) // 20), 20 * 5),
            "keyword": "", "order": "mtime", "type": 0, "tid": 0,
        })
        return (data or {}).get("medias")

    def search(self, query: str, kind: str = "video", limit: int = 10):
        data = self._call("search", {
            "search_type": {"video": "video", "up": "bili_user"}[kind],
            "keyword": query, "page": 1,
        })
        results = (data or {}).get("result") or []
        return results[:limit]

    def video(self, bvid: str):
        return self._call("view", {"bvid": bvid})

    def subtitle(self, bvid: str, page: int = 1):
        view = self._call("view", {"bvid": bvid})
        pages = view.get("pages") or [{}]
        cid = pages[min(page, len(pages)) - 1].get("cid")
        player = self._call("player", {"bvid": bvid, "cid": cid})
        subs = ((player.get("subtitle") or {}).get("subtitles")) or []
        if not subs:
            return {"cid": cid, "subtitles": []}
        # 首个字幕轨道正文（列表按站方排序，lan 字段含语言码）
        url = subs[0]["subtitle_url"]
        if url.startswith("//"):
            url = "https:" + url
        doc = self.s.get(url, timeout=15).json().get("body") or []
        return {
            "cid": cid, "lan": subs[0].get("lan"), "lines": len(doc),
            "text": "\n".join(line.get("content", "") for line in doc),
        }

    def up_info(self, mid: int):
        return self._call("up_info", {"mid": mid, **self._DM_PARAMS},
                          headers=self._space_headers(mid))

    def up_arcs(self, mid: int, limit: int = 20):
        data = self._call("up_arc", {
            "mid": mid, "pn": 1, "ps": min(limit, 50),
            "order": "pubdate", "platform": "web", "jsonp": "jsonp",
            **self._DM_PARAMS,
        }, headers=self._space_headers(mid))
        vlist = ((data or {}).get("list") or {}).get("vlist") or []
        return vlist[:limit]

    # -- 写（低危白名单；--yes 门在 cli 层） -------------------------------

    def watchlater_add(self, bvid: str):
        aid = self._bvid_to_aid(bvid)
        return {"ok": bool(self._call("watchlater_add", post=True, extra_form={"aid": aid}))}

    def watchlater_del(self, bvid: str):
        aid = self._bvid_to_aid(bvid)
        return {"ok": bool(self._call("watchlater_del", post=True, extra_form={"aid": aid}))}

    def fav_add(self, bvid: str, fid: int):
        rid = self._bvid_to_aid(bvid)
        return self._call("fav_deal", post=True, extra_form={
            "rid": rid, "type": 2, "add_media_ids": fid, "del_media_ids": "", "media_id": fid,
        })

    def fav_del(self, bvid: str, fid: int):
        rid = self._bvid_to_aid(bvid)
        return self._call("fav_deal", post=True, extra_form={
            "rid": rid, "type": 2, "add_media_ids": "", "del_media_ids": fid, "media_id": fid,
        })

    def like(self, bvid: str):
        return self._call("like", post=True, extra_form={"bvid": bvid, "like": 1})

    def _bvid_to_aid(self, bvid: str) -> int:
        return int(self._call("view", {"bvid": bvid}).get("aid") or 0)

    # -- 透传 -------------------------------------------------------------

    def raw(self, url: str, post: bool = False):
        r = (self.s.post if post else self.s.get)(url, timeout=20)
        try:
            return r.json()
        except ValueError:
            return {"http_status": r.status_code, "text_head": r.text[:2000]}
