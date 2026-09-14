# todo：临时记忆

跨 session 的委托队列：用户说「明天提醒我选课」，信息在本页存活到被消费。新 session 按 SASU-L 拿不到旧对话（system prompt / AGENTS / skills / user prompt 都不携带），本页 + AGENTS 注入行指针是 L 层的挂载点。本质是**未来时刻的指针集合**——受托即写下「何时读到此条则行动」，agent 是指针执行器。

## Structure

- `wiki/todo.md` 单页（type: todo），首次受托自建；条目 = 列表项 `- [ ] 触发：内容（by, at）`，触发分日期（YYYY-MM-DD，机械可扫描）与情境（语义激活）两类
- 零页面字段：条目级 by/at 用全局 actor 约定（registry 头部）；销账历史写入 `wiki/log.md`——跨进 log 插件领地，是 depends log 的原因

## Invariants

- 条目完整生命周期：受托 → 触发（提醒）→ 销账（`[x]` + log 行）→ 清理（已结 ≤20 静默删，log 已有记录）；全库第一个可销账页面——log 只增、notes 只增、profile 收敛留痕，唯 todo 有销账语义
- 本页只留活工作集，历史归 log：销账事件即记（类型 todo），清理无事件不记
- 有价值的委托完成时走 save 沉淀为知识，本页不管历史
- 读取优先序：新 session 先读本页（先于 hot）——可能有到期委托需主动行动，hot 只是上下文预热
- 不挂命令（模式例外，设计裁定）：条目格式极简、无管道联动，读写契约由注入行自带

## Changelog

- 0.1（2026-09-14）立设：`wiki/todo.md` 委托队列（type: todo 入 registry 领地值）；销账历史归 log（log 类型值集扩 todo）；不挂命令——写入契约由注入行自带
