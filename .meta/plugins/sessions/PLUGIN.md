# sessions：原生会话

会话沉淀的骨干结构：一次工作会话（人或 agent 协作）的知识以骨干页归档，高价值主题提升为独立笔记。原 wiki 思想中 sessions 是一等区，2026-09-08 并入 notes 时降格为 type、结构规范寄居 save 命令；本插件立设后结构归位，命令回归纯操作。

## 结构

- `wiki/sessions/**`，默认命名 `YYYY-MM-DD-<主题>.md`
- type: session（值集见 registry）；participants 必填：YAML 列表，actor 约定（human:名字 / process:流程名 / agent/模型标识）——单 agent 亦记，多 agent 协作直接扩展此列表
- 骨干页形状：核心结论 / 决策与理由 / 非显然洞见 / 开放问题 / 相关页（提升出的主题以 wikilink 挂接）
- 提升规则：独立高价值主题升为 `wiki/notes/` 页（出身是知识，非会话记录），骨干页留 wikilink

## 不变量

- 不可再生区：管道与命令只增不改
- 领地边界与 notes 互补：type: session 必落 `wiki/sessions/`，其余原生笔记落 `wiki/notes/`
- 提升出的页面属 notes 领地，本插件只拥有骨干页

## 检查（注入 check）

- 机械项（audit 覆盖）：session 型页面在 `wiki/sessions/` 之外（或反向）→ warning；participants 缺失或项不符 actor 约定 → warning
- 语义：骨干页过度膨胀（该提升未提升）→ warning

## 注入

AGENTS.md 一行：原生会话区语义。

## 附件

无。

## 变更记录

- 0.1（2026-09-10）立设：自 save 命令长会话段与 notes 合并区抽出（2026-09-08「细分第二批」回归）；领地 `wiki/sessions/`，participants 用 actor 约定留多 agent 扩展点
