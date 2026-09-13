---
name: query
owner: framework
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

- 写 log 一行走管道：`python .meta/scripts/pipeline.py log query "<一句话主题>"`（滚动窗口与归档由脚本机械执行）——读热度由此可测
- log 行即数据区变更：按提交纪律随即提交（`检索: <主题>`，见 `.meta/protocol/actions.md`），不攒批
