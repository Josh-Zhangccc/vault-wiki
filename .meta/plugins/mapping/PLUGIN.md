# mapping：代理层桥

把根目录 `vault/`（概念归 vault 插件）中的每个文件映射为 `wiki/vault/` 的 wiki 代理页。桥接件：语义依赖两端概念插件（vault 与 wiki），depends 显式声明。代理是「资产在 md 世界的代表」：登记 + 一行描述起步，摘要是可选增强。哈希是失配探测器，不是执法器——原文变化的处置走 check 分诊。

## Structure

- `wiki/vault/**` 与 `vault/**` 一比一镜像：路径同构，代理文件名 = 原文件全名 + `.md`（如 `a.pdf` → `a.pdf.md`，防同名碰撞）
- md 文件同样有代理，无特例

## Invariants

- 路径即出身证明：`wiki/vault/` 下页面必有 vault 对应物；出身二分的概念归 wiki 插件。保留名 `index.md` 豁免——目录索引属导航层，非概念页，无 vault 对应物不算孤儿代理
- 登记字段（raw_file / raw_sha256）可从 vault 机械重算
- 代理页属可再生区：管道可重跑覆盖，珍贵内容写入 notes，不留在代理页
- 代理正文不得复制原文全文

## Changelog

- 0.5（2026-09-13）usage 吸收日记类豁免（自 map 命令禁则移入，消正文回声）
- 0.4（2026-09-13）注入源移交 manifest：删 Fields / Checks / Usage / Inject / Attachments 节，md 回归纯文档
- 0.3（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.2（2026-09-12）命令 ingest 更名 map 并瘦身：打磨询问移除（纯登记；vault 治理另议）
- 0.1（2026-09-12）自 vault 插件更名立设（版本重起，旧史见 git）：语义依赖 vault+wiki；「命令对 vault 只增，删改自由属于人」条款移交 vault 概念插件注入行；出身二分概念移交 wiki 插件
