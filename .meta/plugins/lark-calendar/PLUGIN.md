# lark-calendar：lark 日历源

## 设计概要

- **为什么存在**：calendar 的首个源适配器——把 lark-cli 可达的飞书日历投影进时间领地。桥接件形态：语义依赖两端概念插件（calendar 与 lark），无自有领地，全部产出 = **源语法与拉取纪律**
- **关键裁定**：
  - 只写月页 `## 日程` 节（行尾标源键）：不碰手记节、不碰已冻结月页——写边界窄到节级
  - 源语法 `lark/<profile> <calendar_id|primary>`：profile 须为 wiki/lark/ 现役目录——源声明即可达性证明
  - 日更节奏 = 部署侧 cron 无人值守会话（全机械，失败源 log 报告不阻断他源）——多源合流容错的一环

## Structure

- 声明页源语法：`calendar` 块映射值 = `lark/<profile> <calendar_id|primary>`——profile 须为 `wiki/lark/` 现役目录（= cli profile 名）；多日历逐源声明
- 拉取：`lark-cli --profile <名> calendar …`（events instance_view 按当月 / 下月窗口；+agenda 快览）

## Invariants

- 只写月页 `## 日程` 节（行尾标源键）；不碰手记节、不碰已冻结月页
- 全程 `--profile` 必带；auth 现查；写入走 calendar usage 的同步纪律（verify + log + 提交）
- 无自有页面与字段——源语法与拉取纪律是全部产出

## Changelog

- 0.1（2026-09-19）立设：lark 日历源接入 calendar（首个源适配器；日更 = 部署侧 cron 定时无人值守会话）
