# notes：原生笔记

出身就在 wiki 的知识：概念、问答、决策、会话沉淀。它们的「原文」就是 wiki 自身，VAULT 中无对应物。

## 结构

- `wiki/notes/**`，文件名自由（人起名，与镜像区的机械命名相对）
- 细分靠 `type` 字段（qa / concept / comparison / decision / session，开放枚举），不靠目录

## 不变量

- 不可再生区：管道与命令不得覆盖重写既有笔记，只能新增或人手改
- 与 vault 代理层的边界由路径证明：wiki/vault/ 必有对应物，wiki/notes/ 必无

## 检查（注入 check）

- 笔记被命令覆盖的痕迹 → error
- 近似重复笔记（Jaccard > 0.7）→ warning

## 注入

AGENTS.md 一行：原生笔记语义。

## 附件

无。

## 变更记录

- 0.1（2026-09-08）自原 wiki concepts/questions/comparisons/sessions 诸区合并简化（细分第二批）
- 0.2（2026-09-09）孤儿检查移交 link 插件（图性质归链接层）
- 0.3（2026-09-10）manifest 增 layer: origin（分层立设：出身层，零依赖）
