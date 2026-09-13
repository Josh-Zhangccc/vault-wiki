# index：索引

派生层聚合页：检索的便宜入口（query 命令的第二层）。每目录一份，渐进披露——agent 从根索引逐层下钻，不必全库进 context。

## Structure

- 每目录一份 `index.md`（保留名）：根 `wiki/index.md` 带 `format_version` frontmatter（页面格式契约版本，不兼容变更时进位——根索引即版本自述处），只列顶层概念与子目录入口；各子目录（notes/、vault/<子目录>/……）各自的 index 只管本层
- 条目 = wikilink + 描述（frontmatter `description` 字段优先，缺失取正文首个非空非结构行截 80 字）；概念页按 type 分组，子目录条目带子树页面计数
- `wiki/tags.md`：tag → 页面反向索引（聚合 tag 插件的字段）

## Invariants

- 索引页全部可再生、永不手编：只聚合、不原创
- 与实际页面集一致；保留名文件（index / log）、wiki 根派生页（hot / tags）、archive/ 子树不视为概念页、不入索引
- 重建走确定性脚本：`pipeline.py index`（幂等；LLM 不手写索引）

## Changelog

- 0.9（2026-09-13）format_version 语义入库内披露（专家评审：实例内无溯源）；索引描述截断补省略号（pipeline `_cut`）
- 0.8（2026-09-13）注入源移交 manifest：删 Checks / Usage / Inject / Attachments 节，md 回归纯文档
- 0.7（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.6（2026-09-13）根索引版本自述字段更名 format_version（格式契约内化，插件清零外部契约引用）
- 0.5（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.4（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.3（2026-09-10）每目录化（渐进披露）：根页带版本自述字段、子目录带计数；重建脚本化（pipeline.py index/tags，LLM 不手写）
- 0.2（2026-09-10）manifest 增 layer: derived（分层立设：派生层，只向下依赖 tag）
- 0.1（2026-09-08）自原 wiki index（master catalog）规则转化；改为只整体重建、不增量写
