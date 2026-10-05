"""bili-cli 常量：端点表、请求头、本机凭据路径。

端点均为 web 端非公开 API，B 站随时可能改版——以实测为准，未覆盖面走 raw 透传探路。
"""

from pathlib import Path

APP_URL = "https://www.bilibili.com"
API_BASE = "https://api.bilibili.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# 本机凭据（0600，永不入库、永不落屏）
CONFIG_DIR = Path.home() / ".bili-cli"
COOKIE_FILE = CONFIG_DIR / "cookies.json"

# 登录态所需最小 cookie 键；buvid3 缺席时经 spi 端点现补（风控基础）
AUTH_KEYS = ("SESSDATA", "bili_jct")
BUVID_KEYS = ("buvid3", "buvid4")

# endpoint -> (路径, 是否需 WBI 签名)
ENDPOINTS = {
    "nav": ("/x/web-interface/nav", False),            # 我的信息 + WBI 密钥源
    "spi": ("/x/frontend/finger/spi", False),          # buvid 现补，免登录
    "watchlater": ("/x/v2/history/toview/web", False),
    "watchlater_add": ("/x/v2/history/toview/add", False),   # POST aid
    "watchlater_del": ("/x/v2/history/toview/del", False),   # POST aid
    "history": ("/x/v2/history", False),               # GET ps/max 翻页
    "fav_folders": ("/x/v3/fav/folder/created/list-all", False),
    "fav_list": ("/x/v3/fav/resource/list", False),    # GET media_id/pn/ps
    "fav_deal": ("/x/v3/fav/resource/deal", False),    # POST 增删收藏
    "like": ("/x/web-interface/archive/like", False),  # POST bvid/like + csrf
    "search": ("/x/web-interface/search/type", True),  # search_type=video|bili_user
    "view": ("/x/web-interface/view", False),          # 视频详情 bvid
    "player": ("/x/player/wbi/v2", True),              # 字幕字典 bvid/cid
    "up_arc": ("/x/space/wbi/arc/search", True),       # UP 主投稿 mid/pn
    "up_info": ("/x/space/wbi/acc/info", True),        # UP 主信息 mid
    "conclusion": ("/x/web-interface/view/conclusion/get", True),  # 官方 AI 视频总结
}
