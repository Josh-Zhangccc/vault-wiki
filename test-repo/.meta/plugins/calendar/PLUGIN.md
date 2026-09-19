# calendar：时间领地

wiki 的时间维度：何时有何事。事件是行不是页——日历只登记时间线（月页），有分量的事件经 save 沉淀为 note / session 再从日历行 wikilink 过去。源模型开放：manual 手记 + 各适配器（如 lark-calendar）投影，同页汇流——时间是跨租户的单一维度，多源合流正是本领地的存在理由。与 todo 的边界：日历存「何时有何事」，todo 存「何事待办」；事件可派生 todo，反向不合并。

## Structure

- `wiki/calendar.md`——声明页（type: calendar）：frontmatter `calendar` 块映射 = 源键 → 源声明（值语法归适配器，如 `lark/<profile> <calendar_id>`）；正文放使用说明；manual-only 时可缺
- `wiki/calendar/<YYYY-MM>.md`——月页，一页一月（ASCII 文件名）；**两节制**：`## 日程`（源投影区，整节可再生重刷）与 `## 手记`（人 / agent 手写，只增）
- 事件行：`- MM-DD HH:MM~HH:MM 标题（源键）` + 可选 wikilink（人物 / 群档 / 笔记）；全天事件写 `MM-DD 全天`

## Invariants

- 未来滚动、过去冻结：月份走完即冻结，月页不再改写（改写痕迹 → error，git 审计）；错过的变更记入新月页，历史保持如实
- 重刷只整节替换 `## 日程`；手记节永不被源同步触碰
- 月页挂 trust：stale_after 短 TTL（默认 2 天，日更节奏留余量）
- 事件不建页；会议结论归群档议题记录 / notes，日历行只留链接
- 声明页源清单是实例配置；无声明页 = manual-only，合法常态

## Changelog

- 0.1（2026-09-19）立设：月页两节制 + 源开放模型 + 冻结制；lark-calendar 为首个源适配器
