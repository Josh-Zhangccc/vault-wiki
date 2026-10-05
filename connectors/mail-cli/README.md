# mail-cli

wiki email 域的连接器（多 provider：Microsoft Graph / Gmail API / IMAP），OAuth2 device flow 或授权码登录。契约见 `.meta/plugins/email/`。

## 纪律

- 读侧只读：拉信不隐式标已读（Graph GET / IMAP `BODY.PEEK`），不移动不归档不删除
- 凭据只存本机 `~/.config/mail-cli/`（0600），不入库；GCP OAuth 客户端同样只落本机 `gcp.json`
- 发送策略门（见下）：发送类操作在连接器层被人工配置的策略管制

## 用法

`--account` 即插件契约的账户（= `wiki/email/<账户>/` 目录名 = profile 名）。

```
mail-cli auth start  --account <名> [--provider graph|gmail] [--send]  # device flow（graph）/ loopback（gmail）；graph 默认仅申请 Mail.Read 只读 scope（只读 consent 面通常无需管理员审批），--send 才含写/发
mail-cli auth setup  --account <名> --user <地址> --auth-code <码> [--imap-host H] [--smtp-host H]  # imap（如 163）
mail-cli auth status --account <名>
mail-cli profiles                                 # 账户清单（速写遍历入口）
mail-cli folders --account <名> [--all]           # 文件夹/标签（imap 自动解码中文 UTF-7 文件夹名）
mail-cli fetch --account <名> [--folder F] [--since D | --days 7] [--from A]
                [--unread] [--headers] [--limit 30] [--next <url>]
mail-cli read --account <名> --id <id> [--text]   # 单封正文；--text 抽纯文本
mail-cli search --account <名> --query <q> [--limit 10]
mail-cli attach ls  --account <名> --id <id>
mail-cli attach get --account <名> --id <id> --att <aid> [--name 文件名] --dest <目录>
mail-cli draft create --account <名> --to A[,B] [--cc] [--subject S] [--body T | --body-file F]
                       [--html] [--attach 路径]... [--reply-to <msg-id>]   # 回复自动带线程头
mail-cli draft list/show/delete --account <名> --id <草稿id>（list 无 --id）
mail-cli send --account <名> --id <草稿id> [--yes]
```

输出恒为单行 JSON。graph/gmail token 到期自动续期。

## 发送策略（人工配置，连接器只读）

`~/.config/mail-cli/policy.json`，人手编辑，**缺席 = 全部 deny**：

```json
{"<账户>": {"send": "deny|confirm|auto", "auto_allow": ["白名单地址"]}}
```

- `deny`：send 一律拒绝（草稿可建）
- `confirm`：TTY 回车确认；非 TTY 须 `--yes`（= 用户已在对话明示，agent 只是执行已给出的同意）
- `auto`：直接放行；配 `auto_allow` 时仅白名单收件人放行，其余落回 confirm

## Provider 路线与实测坑

| provider | 认证 | 路线 | 已知坑 |
|---|---|---|---|
| graph（Microsoft/学校） | device flow | Graph API v1.0 | `internetMessageHeaders` 只能 `$select` 不能 `$expand`；学校租户写权限可能要管理员审批 |
| gmail | loopback（ssh -L 隧道收回调） | Gmail API v1 | **device flow 不放行 Gmail scope**（invalid_scope，TV 客户端也不行）；须桌面客户端 + 本机起临时 HTTP 服务 |
| imap（163 等） | 授权码（auth setup） | IMAP4_SSL + SMTP_SSL，标准库 | **163 须发 IMAP ID 自报身份**否则 select 报 Unsafe Login；中文文件夹名为 modified UTF-7（已解码）；中文搜索词退回客户端过滤（imaplib 参数仅 ascii） |

## 依赖

无（Python 3 标准库）。graph 借用 Microsoft Graph PowerShell 公开 client；gmail 需自备 GCP OAuth 客户端（`gcp.json`）。

## Changelog

- 0.4 2026-10-05：graph 最小授权——默认 scope 收敛为 `Mail.Read offline_access`（读信不再触发写/发 consent 面与随之而来的管理员审批），`auth start --send` 显式申请宽 scope；token 记录已授 scope（刷新保面），draft create/delete 与 send 在只读凭据下提前拒绝（token_read_only）
- 0.3 2026-10-05：多 provider（graph/gmail/imap）；发送策略门 policy.json（deny/confirm/auto + 白名单）；draft 全套与 send（graph createReply / gmail threadId / imap In-Reply-To 线程头）；163 IMAP ID 与 UTF-7 文件夹解码；gmail loopback 授权流
- 0.2 2026-10-05：多账户命令面——`--account` 对齐插件契约（原 `--profile`）；新增 profiles / folders / attach ls·get；fetch 增 `--folder/--since/--from/--unread/--headers` 与分页；read 增 `--text` 纯文本抽取与 message-id/references；错误转 JSON 输出
- 0.1 2026-10-05：立设——auth / fetch / read / search，单行 JSON，自动续期
