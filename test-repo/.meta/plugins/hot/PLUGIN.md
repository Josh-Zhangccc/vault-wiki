# hot：热缓存

最近变更的摘要页，agent 进入库的最低成本入口（先读 hot，再按需深入）。

## Structure

- 单文件 `wiki/hot.md`，分节组织（Recent map / Recent save / Recent query / Recent check…）
- 条目：日期 + wikilink + 一句话核心（≤200 字符，硬上限）

## Invariants

- 可整体再生：hot 只是缓存，丢失可从 log 与库中重建
- 滚动窗口：窗外即删；淘汰与截短由脚本机械执行（机械自动，不询问）

## Config

```yaml config
hot.max_entries: 25        # 机械权威源在 pipeline.py（脚本源码即规则清单），本节为语义说明
hot.max_days: 5
hot.max_entry_chars: 200   # 参数依原库实测校准（原库单条中位 389 字、最大 4959 字，失控实证）
```

## Changelog

- 0.10（2026-09-23）补 wiki 依赖边——内侧插件挂 wiki 对齐 domain 0.1 声明（2026-09-22 域化批次漏收）
- 0.9（2026-09-13）usage 类型参数补值集出处（同 log，指向 AGENTS 注入区 log 块）
- 0.8（2026-09-13）注入源移交 manifest：删 Checks / Usage / Inject / Attachments 节，md 回归纯文档
- 0.7（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.6（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.5（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.4（2026-09-10）写入机械化：走 pipeline.py hot（淘汰/截短由脚本执行），参数权威源移交脚本源码
- 0.3（2026-09-10）manifest 增 layer: derived（分层立设：派生层，零依赖）
- 0.2（2026-09-09）单条长度上限 200 字符 + 写前淘汰义务明文化
- 0.1（2026-09-08）自原 wiki hot 结构转化
