# vault：代理层

把根目录 `vault/`（VAULT，真实资产仓库）中的每个文件登记为 wiki 代理页。代理是「资产在 md 世界的代表」：登记 + 一行描述起步，摘要是可选增强。VAULT 的删改不受本插件管理——哈希是失配探测器，不是执法器。

## 结构

- `wiki/vault/**` 与 `vault/**` 一比一镜像：路径同构，代理文件名 = 原文件全名 + `.md`（如 `a.pdf` → `a.pdf.md`，防同名碰撞）
- md 文件同样有代理，无特例

## 不变量

- 路径即出身证明：`wiki/vault/` 下页面必有 VAULT 对应物；不在其下的 wiki 页面是原生笔记（归 notes 插件）
- 登记字段（raw_file / raw_sha256）可从 VAULT 机械重算
- 代理页属可再生区：管道可重跑覆盖，珍贵内容写入 notes，不留在代理页
- 代理正文不得复制原文全文

## 自有字段

`raw_file`（根相对路径）、`raw_sha256`

## 检查（注入 check）

- VAULT 有文件而无代理 → warning（待登记）
- 代理无 VAULT 对应物（孤儿）→ error
- raw_sha256 与 VAULT 实际哈希失配 → warning（原文已被改动；报告，由人决定重摄入或删代理）
- 代理正文复制原文全文 → error；正文无一行描述（stub）→ warning

## 注入

AGENTS.md 一行：代理层语义与出身规则。

## 附件

无包内附件。

## 变更记录

- 0.1（2026-09-08）自原 wiki sources 结构与 vault-ingest 契约转化
