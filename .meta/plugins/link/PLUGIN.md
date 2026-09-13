# link：链接层

wiki 的本体结构：页面间的引用关系。链接是知识的价值所在——思维发生在碰撞处。本插件拥有链接语法与关系字段，并托管图性质的健康检查（断链 / 孤儿）。

## Structure (no own files)

- `related` 字段：YAML 列表，本页主题相关页面的全名（wikilink）
- `aliases` 字段：YAML 列表，本页别名 / 短名，供链接解析与检索
- wikilink 语法约定：`[[页面全名]]`；禁止截断式部分引用（长复合名必须写全）；同名歧义时带路径

## Invariants

- 链接目标必须可解析：全名命中页面，或命中某页的 aliases
- 断链不静默但不当畸形处理：断链可能是尚未写下的知识，TODO 占位属正常形态；拿不准目标时宁可留 TODO 也不猜
- 孤儿判定是图性质：无入链且无 related 引用的页面才算孤儿；**入链源只计概念页**——index / hot / log / tags 与 archive/ 等派生页不算链接源（否则索引链接一切，孤儿永不触发）

## Checks

- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：断链（目标既非页面全名，也非任何页的 aliases）→ warning；乱码链接（目标含 U+FFFD 替换符，含 related 项）→ error；别名二义（两页声明同一 aliases，解析不确定）→ error；孤儿页（无入链且无 related 引用，入链源只计概念页）→ warning；related 单向（A 列 B 而 B 未回列）→ 信息
- 语义项（check 命令）：入链密度 top 榜 → 信息项（hub 涌现依据，不告警）

## Inject

AGENTS.md 一行：链接语法与解析规则。

## Attachments

无 wiki 附件；附检脚本 `scripts/check.py`（机械检查项，audit 发现式执行）。

## Changelog

- 0.6（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.5（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-09）新立：链接语法与 related / aliases 字段；断链检查自原 lint 转化，孤儿检查自 notes 移交
- 0.2（2026-09-10）manifest 增 layer: field（分层立设：字段层，零依赖）
- 0.3（2026-09-10）断链降级 warning（对齐 OKF：尚未写下的知识）；孤儿判定作用域明文（派生页不算入链源）
- 0.4（2026-09-11）机械项收编附检脚本：断链 / 乱码 / 孤儿 / 新增别名二义（error）与 related 单向（信息）；hub 榜留语义项
