# mail-cli

wiki email 域的最小只读连接器（Microsoft Graph, OAuth2 device flow）。契约见 `.meta/plugins/email/`。

## 纪律

- 只读：Graph GET，拉信不隐式标已读（PEEK 语义），不移动不归档不删除
- 凭据只存本机 `~/.config/mail-cli/<profile>.json`，不入库
- 发送类操作不支持——红线在插件层，连接器无此能力

## 用法

```
mail-cli auth start --profile <名>            # 发起 device flow，输出 verification_url + user_code
mail-cli auth complete --profile <名>          # 轮询至用户在浏览器确认（--device-code 可显式传入）
mail-cli auth status --profile <名>            # 登录态与账户
mail-cli fetch --profile <名> [--folder inbox] [--days 7] [--limit 30]
mail-cli read --profile <名> --id <message-id> # 读单封正文（截断 8000 字）
mail-cli search --profile <名> --query <词> [--limit 10]
```

输出恒为单行 JSON。token 到期自动用 refresh_token 续期。

## 依赖

无（Python 3 标准库）。client_id 借用 Microsoft Graph PowerShell 公开 client（TENANT=common，scope `Mail.Read offline_access`）。
