# lark-docs：云文档域

服务 profile 抽象的域插件：飞书云文档（知识库 / 云盘）的访问与映射。全量映射明令禁止——云文档量大且用户只关心局部，枚举只服务两件事：枢纽页的「结构速写」与关心区的解析；指针页仅落关心区内对象。

## Structure

- `<profile>/docs.md`（kind: docs）——域枢纽：frontmatter `docs` 块映射 = 关心区→范围一句话（实例配置，人可改 agent 可读）；正文「云盘结构速写」（agent 蒸馏：知识空间清单 / 顶层目录 / 一句话，带 stale_after，非镜像）
- `<profile>/docs/<关心区>/…`——指针页子树，关心区一层、往下平铺容忍
- kind 词表（开放，跟 lark obj_type）：docx / wiki / sheet / base / file / …

## Invariants

- 全量映射禁止；关心区是映射的唯一入口
- 结构速写是蒸馏产物，过期走 stale_after，不追求与 lark 侧实时一致
- 指针页正文一行摘要起步；快照节 `## 快照 YYYY-MM-DD` 选段追加、禁全文复制
- TTL 默认 7 天（profile.md 可覆写）

## Changelog

- 0.1（2026-09-19）立设：docs.md 三件套（结构速写 / 关心区 / 按区映射）
