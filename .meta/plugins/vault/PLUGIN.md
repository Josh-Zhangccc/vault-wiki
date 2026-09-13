# vault：代理层

把根目录 `vault/`（VAULT，真实资产仓库）中的每个文件登记为 wiki 代理页。代理是「资产在 md 世界的代表」：登记 + 一行描述起步，摘要是可选增强。VAULT 的删改不受本插件管理——哈希是失配探测器，不是执法器。

## Structure

- `wiki/vault/**` 与 `vault/**` 一比一镜像：路径同构，代理文件名 = 原文件全名 + `.md`（如 `a.pdf` → `a.pdf.md`，防同名碰撞）
- md 文件同样有代理，无特例

## Invariants

- 路径即出身证明：`wiki/vault/` 下页面必有 VAULT 对应物；不在其下的 wiki 页面是原生笔记（归 notes 插件）。保留名 `index.md` 豁免——目录索引属导航层，非概念页，无 VAULT 对应物不算孤儿代理
- 登记字段（raw_file / raw_sha256）可从 VAULT 机械重算
- 代理页属可再生区：管道可重跑覆盖，珍贵内容写入 notes，不留在代理页
- 代理正文不得复制原文全文

## Fields

`raw_file`（根相对路径）、`raw_sha256`

## Checks

- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：镜像 diff（VAULT 有文件无代理 → 信息积压；代理无对应物 → error）、raw_file 悬挂 → error、raw_sha256 失配 → warning、疑似全文复制（md 资产正文 ≥80% 原文）→ warning、无描述 stub 且 updated 超 90 天 → warning
- 语义项（check 命令）：失配处置分诊（描述仍适用 → 机械重算自动修复；疑似失效 → 人决重摄入或删）；日记类全文复制豁免判断

## Inject

AGENTS.md 一行：代理层语义与出身规则。

## Attachments

无包内附件。

## Changelog

- 0.7（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-08）自原 wiki sources 结构与 vault-ingest 契约转化
- 0.2（2026-09-09）检查分诊对齐动作纪律：哈希重算自动化、stub 按年龄告警、积压计数信息化
- 0.3（2026-09-09）机械检查项落为附检脚本（scripts/check.py），本文件保留语义项
- 0.4（2026-09-10）manifest 增 layer: origin（分层立设：出身层，零依赖）
- 0.5（2026-09-10）镜像豁免保留名 index.md（index 插件每目录化后 wiki/vault/ 出现目录索引页）
- 0.6（2026-09-11）manifest 增 commands: [ingest]（命令-插件绑定显式化：ingest 由本插件驱动）
