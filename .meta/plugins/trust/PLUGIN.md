# trust：信任字段

知识会老化。本插件拥有四个信任字段（原 registry 预留段回填认领），让「这条知识还可信吗」从通读原文变成读字段；层级推导是读取时的纯计算，不落盘。

## Structure (no wiki files)

- `generated`：块式映射 `by / at`（actor 约定 + YYYY-MM-DD）——页面由谁生成；map / save 写代理页与笔记时随手写
- `verified`：事件列表，项单行 `by: <actor>, at: <日期>`；可多次追加（复核历史）；谁可写：human 复核、agent/process 机械核验（如哈希重算）
- `stale_after`：YYYY-MM-DD 绝对时刻；语义是「此后无人复核就应视为过期」，刷新它 = 一次续期决策
- `sources`：来源列表，项含 id / resource / 可信度信号（author、usage_count、last_modified）

## Example (trust fields)

```yaml
generated:
  by: agent/GLM-5.3
  at: 2026-09-12
verified:
  - "by: process:hash-recalc, at: 2026-09-12"
  - "by: human:Joss, at: 2026-09-12"
stale_after: 2026-12-31
sources:
  - id: 雾港设计备忘
    resource: vault/雾港/设计备忘.md
    author: human:Joss
    usage_count: 3
    last_modified: 2026-09-05
```

上例水位 = human-reviewed（含 human 事件）；2026-12-31 之后读取显示 stale。四字段全部可选，通常只写 `generated`。

## Level Derivation (computed on read, never persisted)

- **unverified**：无 verified 记录
- **machine-confirmed**：仅含 agent / process 事件
- **human-reviewed**：含 human 事件（最高级）
- **stale**：now ≥ stale_after——独立于上述层级，覆盖显示

推导禁止生成派生页：可再生区不造第二份会漂移的真相，消费方（query / check / viewer）按上表现算。

## Invariants

- verified 事件只追加不改写（事件是历史）；追加由复核动作触发，不为凑水位伪造
- 层级与 stale 判定均为纯比较，无隐藏状态
- 字段全部可选：不写 = unverified，不阻断任何读写

## Checks

- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：generated 缺 by/at 或 actor 格式错、verified 事件缺 by/at 或格式错、stale_after 非 YYYY-MM-DD、sources 非列表 → warning
- 机械项（信息级）：stale 页清单（已过 stale_after）；信任水位（human-reviewed / machine-confirmed 计数）
- 语义（check 命令）：stale 页处置分诊（刷新时刻 / 重验证 / 废弃）——人决

## Inject

AGENTS.md 一行：信任字段与层级推导。

## Attachments

无 wiki 附件；附检脚本 `scripts/check.py`。

## Changelog

- 0.3（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-11）立设：认领 registry 预留段四字段（generated / verified / stale_after / sources）回填插件段；层级推导不落盘；附检覆盖字段契约 + stale 清单 + 信任水位
- 0.2（2026-09-12）披露修补：内联四字段全形状样例（冷启动审计猜点：规格无实例）
