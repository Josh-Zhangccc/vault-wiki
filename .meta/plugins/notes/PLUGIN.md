# notes：原生笔记

出身就在 wiki 的知识：概念、问答、决策、实体。它们的「原文」就是 wiki 自身，vault 中无对应物。会话骨干页不在本区——归 sessions 插件。

## Structure

- `wiki/notes/**`，文件名自由（人起名，与镜像区的机械命名相对）
- 细分靠 `type` 字段（值集以 registry 为准，扩值须修订注册表），不靠目录

## Invariants

- 不可再生区：管道与命令不得覆盖重写既有笔记，只能新增或人手改
- 与 vault 代理层的边界由路径证明：wiki/vault/ 必有对应物，wiki/notes/ 必无
- 与 sessions 的边界由 type 证明：type: session 落 `wiki/sessions/`，不落本区

## Checks

- 笔记被命令覆盖的痕迹 → error
- 近似重复笔记（Jaccard > 0.7）→ warning

## Usage

- 落点 `wiki/notes/<标题>.md`，文件名自由（人起名）；type 取 qa / concept / comparison / decision / entity（值集见 registry）
- 只增：更新既有笔记属人手改，命令不覆盖重写

## Inject

AGENTS.md 一行：原生笔记语义。

## Attachments

无。

## Changelog

- 0.9（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.8（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.7（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-08）自原 wiki concepts/questions/comparisons/sessions 诸区合并简化（细分第二批）
- 0.2（2026-09-09）孤儿检查移交 link 插件（图性质归链接层）
- 0.3（2026-09-10）manifest 增 layer: origin（分层立设：出身层，零依赖）
- 0.4（2026-09-10）type 枚举表述修正：以 registry 值集为准（消与注册表封闭性的矛盾）
- 0.5（2026-09-10）缩界：会话骨干页移交 sessions 插件（独立领地 `wiki/sessions/`），本区留概念/问答/决策/实体
- 0.6（2026-09-11）manifest 增 commands: [save]（save 由本插件与 sessions 共同驱动）
