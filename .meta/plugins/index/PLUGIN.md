# index：索引

派生层聚合页：检索的便宜入口（query 命令的第二层）。每目录一份，渐进披露——agent 从根索引逐层下钻，不必全库进 context。

## Structure

- 每目录一份 `index.md`（保留名）：根 `wiki/index.md` 带 `format_version` frontmatter，只列顶层概念与子目录入口；各子目录（notes/、vault/<子目录>/……）各自的 index 只管本层
- 条目 = wikilink + 描述（frontmatter `description` 字段优先，缺失取正文首个非空非结构行截 80 字）；概念页按 type 分组，子目录条目带子树页面计数
- `wiki/tags.md`：tag → 页面反向索引（聚合 tag 插件的字段）

## Invariants

- 索引页全部可再生、永不手编：只聚合、不原创
- 与实际页面集一致；保留名文件（index / log）、wiki 根派生页（hot / tags）、archive/ 子树不视为概念页、不入索引
- 重建走确定性脚本：`python .meta/scripts/pipeline.py index`（幂等；LLM 不手写索引）

## Checks

- 索引与实际页面集偏差 → 跑 `pipeline.py index` 重建即修复（幂等，无 diff 即一致）；tags 同理（`pipeline.py tags`）
- 手编痕迹 → warning

## Inject

AGENTS.md 一行：检索入口指针。

## Attachments

无（重建逻辑在 `.meta/scripts/pipeline.py`，与 hot / log 共用管道）。

## Changelog

- 0.6（2026-09-13）根索引版本自述字段更名 format_version（格式契约内化，插件清零外部契约引用）
- 0.5（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.4（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-08）自原 wiki index（master catalog）规则转化；改为只整体重建、不增量写
- 0.2（2026-09-10）manifest 增 layer: derived（分层立设：派生层，只向下依赖 tag）
- 0.3（2026-09-10）每目录化（渐进披露）：根页带版本自述字段、子目录带计数；重建脚本化（pipeline.py index/tags，LLM 不手写）
