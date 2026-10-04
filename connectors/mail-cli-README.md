# mail-cli

wiki email 域的最小只读连接器（Microsoft Graph, OAuth2 device flow）。契约见 `.meta/plugins/email/`。

## 纪律

- 只读：Graph GET，拉信不隐式标已读（PEEK 语义），不移动不归档不删除
- 凭据只存本机 `~/.config/mail-cli/<account>.json`，不入库
- 发送类操作不支持——红线在插件层，连接器无此能力

## 用法

`--account` 即插件契约的账户（= `wiki/email/<账户>/` 目录名 = 连接器 profile 名）。

```
mail-cli auth start --account <名>                # 发起 device flow
mail-cli auth complete --account <名>             # 轮询至浏览器确认
mail-cli auth status --account <名>
mail-cli profiles                                 # 账户清单（速写遍历入口）
mail-cli folders --account <名> [--all]           # 文件夹树（--all 递归子层）
mail-cli fetch --account <名> [--folder inbox] [--since D | --days 7] [--from A]
                [--unread] [--headers] [--limit 30] [--next <url>]
mail-cli read --account <名> --id <id> [--text]   # 单封正文；--text 抽纯文本
mail-cli search --account <名> --query <q> [--folder F] [--limit 10]
mail-cli attach ls  --account <名> --id <id>
mail-cli attach get --account <名> --id <id> --att <aid> [--name 文件名] --dest <目录>
```

输出恒为单行 JSON。token 到期自动用 refresh_token 续期。

## 字段与语义

- `fetch` 默认按时间倒序；`--since`（YYYY-MM-DD 或 ISO）与 `--days` 二选一，均转服务端 `$filter`
- `--from` 含 `@` 走服务端精确过滤，否则退回客户端子串匹配
- `--headers` 补 `message_id` / `references`（Message-ID 与 References 链）——立线程档的原料；Graph 实测 `internetMessageHeaders` 只能 `$select` 不能 `$expand`
- `conversationId`（Outlook 会话组）恒返回，作 References 断裂时的兜底聚类信号
- 分页：结果带 `next`，透传给下一次 `--next` 即续拉
- `attach get` 落盘文件名取附件元数据名，`--name` 可覆写；适合 vault 物化后走 map 代理

## 依赖

无（Python 3 标准库）。client_id 借用 Microsoft Graph PowerShell 公开 client（TENANT=common，scope `Mail.Read offline_access`）。

## Changelog

- 0.2 2026-10-05：多账户命令面——`--account` 对齐插件契约（原 `--profile`）；新增 profiles / folders / attach ls·get；fetch 增 `--folder/--since/--from/--unread/--headers` 与分页；read 增 `--text` 纯文本抽取与 message-id/references；错误转 JSON 输出
- 0.1 2026-10-05：立设——auth / fetch / read / search，单行 JSON，自动续期
