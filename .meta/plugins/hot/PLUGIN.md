# hot：热缓存

最近变更的摘要页，agent 进入库的最低成本入口（先读 hot，再按需深入）。

## 结构

- 单文件 `wiki/hot.md`，分节组织（最近摄入 / 最近保存 / 最近检查……）
- 条目：日期 + wikilink + 一句话核心

## 不变量

- 可整体再生：hot 只是缓存，丢失可从 log 与库中重建
- 滚动窗口：窗外即删

## 配置

```yaml config
hot.max_entries: 25
hot.max_days: 5
```

## 检查（注入 check）

- 窗口越界（超 25 条或超 5 日）→ warning
- 与 log 矛盾（log 有记录而 hot 全无踪迹）→ warning

## 注入

AGENTS.md 一行：agent 读取顺序的起点。

## 附件

无。

## 变更记录

- 0.1（2026-09-08）自原 wiki hot 结构转化
