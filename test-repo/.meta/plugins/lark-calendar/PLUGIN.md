# lark-calendar：lark 日历源

桥接件：把 lark-cli 可达的飞书日历投影进 calendar 时间领地——语义依赖两端概念插件（calendar 与 lark，depends 显式声明，拓扑同 mapping 之于 vault+wiki）。无自有领地：页面与格式归 calendar，CLI 纪律归 lark 基座，本插件的全部产出是**源语法与拉取纪律**。

## Structure

- 声明页源语法：`calendar` 块映射值 = `lark/<profile> <calendar_id|primary>`——profile 须为 `wiki/lark/` 现役目录（= cli profile 名）；多日历逐源声明
- 拉取：`lark-cli --profile <名> calendar …`（events instance_view 按当月 / 下月窗口；+agenda 快览）

## Invariants

- 只写月页 `## 日程` 节（行尾标源键）；不碰手记节、不碰已冻结月页
- 全程 `--profile` 必带；auth 现查；写入走 calendar usage 的同步纪律（verify + log + 提交）
- 无自有页面与字段——源语法与拉取纪律是全部产出

## Changelog

- 0.1（2026-09-19）立设：lark 日历源接入 calendar（首个源适配器；日更 = 部署侧 cron 定时无人值守会话）
