# sessions：原生会话

会话沉淀的骨干结构：一次工作会话（人或 agent 协作）的知识以骨干页归档，高价值主题提升为独立笔记。原 wiki 思想中 sessions 是一等区，2026-09-08 并入 notes 时降格为 type、结构规范寄居 save 命令；本插件立设后结构归位，命令回归纯操作。

## Structure

- `wiki/sessions/**`，默认命名 `YYYY-MM-DD-<主题>.md`
- type: session（值集见 registry）；participants 必填：YAML 列表，actor 约定（human:名字 / process:流程名 / agent/模型标识）——单 agent 亦记，多 agent 协作直接扩展此列表
- 骨干页形状：核心结论 / 决策与理由 / 非显然洞见 / 开放问题 / 相关页（提升出的主题以 wikilink 挂接）
- 提升规则：独立高价值主题升为 `wiki/notes/` 页（出身是知识，非会话记录），骨干页留 wikilink

## Example (backbone page)

`wiki/sessions/2026-09-12-雾港美术风格定稿.md`：

```markdown
---
type: session
title: 雾港美术风格定稿
participants: [human:Joss, agent/GLM-5.3]
created: 2026-09-12
tags: [游戏/美术]
---
# 核心结论
低多边形 + 体积雾定稿，进入场景外包询价。

# 决策与理由
像素风被否：剪影可读性差。详见 [[notes/雾港美术风格决策]]。

# 非显然洞见
预算超支风险集中在场景美术外包（报价 16.8 万，超支 40%）。

# 开放问题
体积雾在低端机的性能预算？

# 相关页
- [[notes/雾港美术风格决策]]（本次会话提升出的决策页）
```

## Invariants

- 不可再生区：管道与命令只增不改
- 领地边界与 notes 互补：type: session 必落 `wiki/sessions/`，其余原生笔记落 `wiki/notes/`
- 提升出的页面属 notes 领地，本插件只拥有骨干页

## Checks

- 机械项（audit 覆盖）：session 型页面在 `wiki/sessions/` 之外（或反向）→ warning；participants 缺失或项不符 actor 约定 → warning
- 语义：骨干页过度膨胀（该提升未提升）→ warning

## Inject

AGENTS.md 一行：原生会话区语义。

## Attachments

无。

## Changelog

- 0.4（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-10）立设：自 save 命令长会话段与 notes 合并区抽出（2026-09-08「细分第二批」回归）；领地 `wiki/sessions/`，participants 用 actor 约定留多 agent 扩展点
- 0.2（2026-09-11）manifest 增 commands: [save]（save 由本插件与 notes 共同驱动）
- 0.3（2026-09-12）披露修补：内联骨干页全形状样例（冷启动审计猜点：区内无实例）
