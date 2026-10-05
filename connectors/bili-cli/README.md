# bili-cli

wiki bilibili 域的连接器（web cookie 登录态，自研轻实现：requests + 自实现 WBI 签名，无社区库依赖）。契约见 `.meta/plugins/bili/`。

## 纪律

- **只读为主 + 低危写白名单**（2026-10-06 所有者裁定）：白名单 = 稍后再看增删 / 收藏夹增删 / 点赞，三项均须用户明示动词（agent 层）+ `--yes`（CLI 层）双门；白名单外写操作（投币/评论/转发/关注/私信/弹幕）永不提供、raw 亦不承载
- 凭据即浏览器 cookie（SESSDATA / bili_jct = csrf）：只存本机 `~/.bili-cli/cookies.json`（0600），不入库、不落屏、不回显完整值
- 个人数据（观看历史 / 收藏夹 / 稍后再看）属实例数据：会话内中继即止，永不提交任何仓库

## 用法

```
bili-cli login --cookie "SESSDATA=..; bili_jct=..; buvid3=.."   # 浏览器 DevTools 拷贝导入（或 --file）
bili-cli me                                    # 我的信息（登录自检）
bili-cli fav [--fid <id>] [--limit N]          # 收藏夹清单 / 内容
bili-cli watchlater                            # 稍后再看列表
bili-cli history [--limit N]                   # 观看历史（近窗）
bili-cli search <q> [--kind video|up] [--limit N]
bili-cli video <bvid>                          # 详情：分P/统计/简介
bili-cli subtitle <bvid> [--page N]            # 字幕正文（首个 CC 轨道）
bili-cli up <mid> [--arcs --limit N]           # UP 主信息（+最新投稿）
# 写（白名单，双门）：
bili-cli watchlater add|remove <bvid> --yes
bili-cli fav add|remove <bvid> --fid <id> --yes
bili-cli like <bvid> --yes
bili-cli raw <url> [--post]                    # 透传（探路/对账）
```

输出恒单行 JSON；时间戳 `YYYY-MM-DD HH:MM` 本地时区。

## 实现注记

- WBI 签名：nav 下发 img/sub key → 64 项重排版取前 32 → 参数加 wts 排序 → md5 → `w_rid`；进程内缓存密钥
- buvid3 缺席经 `/x/frontend/finger/spi` 现补（风控基础面）
- 写操作表单自动注 csrf（= bili_jct）
- 端点表集中在 `bilicli/config.py`——B 站改版先改这里，未覆盖面走 raw

## 已知坑（实测回改区）

- 非公开 web API，无稳定性承诺；code -412 = 风控（串行、克制调用）
- 字幕仅 UP 主上传的 CC；AI 自动字幕不在 player 载荷
- search 仅首页；深翻页走 raw
- 登录失效 code -101 → 重新导出 cookie

## Changelog

- 0.1.0 2026-10-06：立设——七项设计决策经用户问答收敛（功能面：个人数据+查询+追踪；web cookie 认证；低危写白名单三项；自研轻实现；先现拉后 cron；查询即答+涌现档案；连接器+域全套）
