# index：索引

聚合各插件字段生成的索引页，检索的便宜入口（query 命令的第二层）。

## 结构

- `wiki/index.md`：全库页面清单，按 type 分组，每行 = wikilink + 一句话
- `wiki/tags.md`：tag → 页面反向索引（聚合 tag 插件的字段）

## 不变量

- 索引页全部可再生、永不手编：只聚合、不原创
- 与实际页面集一致

## 检查（注入 check）

- 索引与实际页面集偏差 → error（重建即修复）
- 手编痕迹 → warning

## 注入

AGENTS.md 一行：检索入口指针。

## 附件

无。

## 变更记录

- 0.1（2026-09-08）自原 wiki index（master catalog）规则转化；改为只整体重建、不增量写
- 0.2（2026-09-10）manifest 增 layer: derived（分层立设：派生层，只向下依赖 tag）
