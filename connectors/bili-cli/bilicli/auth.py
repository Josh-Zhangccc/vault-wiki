"""cookie 导入与加载：SESSDATA/bili_jct（+buvid3），0600 存 ~/.bili-cli/cookies.json。

cookie 即全权凭据——只存本机 CONFIG_DIR，永不入库、永不回显完整值。
"""

import json
import os
import sys

from .config import AUTH_KEYS, COOKIE_FILE


def parse_cookie_string(raw: str) -> dict:
    """解析 "k=v; k2=v2" 形式的 cookie 串（浏览器 DevTools 直接拷贝的 Request Header 值）。"""
    jar = {}
    for part in raw.replace("\n", ";").split(";"):
        if "=" not in part:
            continue
        k, _, v = part.strip().partition("=")
        if k and v:
            jar[k] = v
    return jar


def save_cookies(jar: dict) -> None:
    missing = [k for k in AUTH_KEYS if k not in jar]
    if missing:
        raise SystemExit(f"cookie 缺登录键 {missing}（需 SESSDATA 与 bili_jct，自浏览器 DevTools 拷贝）")
    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_FILE.write_text(json.dumps(jar, ensure_ascii=False, indent=2), encoding="utf-8")
    try:  # 非 Windows 生效；Windows 下 best-effort
        os.chmod(COOKIE_FILE, 0o600)
    except OSError:
        pass


def load_cookies() -> dict:
    if not COOKIE_FILE.exists():
        raise SystemExit("未登录：先 bili-cli login --cookie '...'（或 --file），凭据只存 ~/.bili-cli/")
    return json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
