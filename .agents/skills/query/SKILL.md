---
name: query
owner: framework
consumes: [log]
description: "在 wiki 中检索并综合回答：热缓存→索引→grep→读页，产出带 wikilink 引用的答案。Triggers on: query, what do you know about, what is, explain, find in wiki, 检索."
---

# query：检索

读为主，唯一写动作是 log 一行（读信号）。分层递进，便宜的先上。

## Scope

读：hot、index、tags、页面
写：log（仅一行，type "query"）

## Read Order

1. wiki/hot.md（最近上下文，最便宜）
2. wiki/index.md / wiki/tags.md（目录与 tag 索引）
3. grep（路径 / 标题 / 正文关键词）
4. 读具体页面确认（每次查询 ≤3-5 页）

## Answer Rules

- 中文为主；页名以 wikilink 保留
- 引用内联标注出处
- 与库内既有内容矛盾时明确标出

## Not For

- 不为通用编程问题读库（训练数据已覆盖）
- 不为对话或项目文件已有内容读库

## Wrap-up

- 写 log 一行（读信号，读热度由此可测）：调用方式见注入区 log 块
- log 行即数据区变更：按提交纪律随即提交（`检索: <主题>`，见 `.meta/protocol/actions.md`），不攒批

## Injected Section (plugin usage blocks)

> 本区为 plugin_cli 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:log -->
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>"`；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
