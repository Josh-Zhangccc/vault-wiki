# link：链接层

wiki 的本体结构：页面间的引用关系。链接是知识的价值所在——思维发生在碰撞处。本插件拥有链接语法与关系字段，并托管图性质的健康检查（断链 / 孤儿）。

## Structure (no own files)

- `related` 字段：YAML 列表，本页主题相关页面的全名（wikilink）
- `aliases` 字段：YAML 列表，本页别名 / 短名，供链接解析与检索
- wikilink 语法约定：`[[页面全名]]`；**全名 = 页面文件在 wiki/ 内的相对路径去末尾 .md**（如 `notes/X`；md 资产的代理文件是 `原名.md.md`，全名为 `vault/原名.md`）；禁止截断式部分引用（长复合名必须写全）；同名歧义时带路径

## Invariants

- 链接目标必须可解析：全名命中页面，或命中某页的 aliases
- 断链不静默但不当畸形处理：断链可能是尚未写下的知识，TODO 占位属正常形态；拿不准目标时宁可留 TODO 也不猜
- 孤儿判定是图性质：无入链且无 related 引用的页面才算孤儿；**入链源只计概念页**——index / hot / log / tags 与 archive/ 等派生页不算链接源（否则索引链接一切，孤儿永不触发）；领地值页（registry 领地值除 session——source / lark / calendar / structure / todo / profile，机械登记类）暂无入链是登记常态，降为信息级，notes 知识页保持 warning；hot 是唯一手写链接的派生页，断链受检但不作入链源

## Changelog

- 0.12（2026-09-19）孤儿 info 集改动态读 registry type.values（除 session）——新领地类型自动覆盖，硬编码集退役（project 立设前置）
- 0.11（2026-09-19）孤儿 info 集扩至全部领地值（除 session）——calendar 冒烟实锤 calendar.md/月页误报 warning；判定与 registry 领地值对齐，不再逐类型挤牙膏
- 0.10（2026-09-19）孤儿降级判定路径制改 type 制（source / lark 同待遇）——lark 族落地冒烟实锤：新指针页全量误报 warning
- 0.9（2026-09-13）附检补 hot 手写断链扫描；孤儿分级——代理页降 info（专家评审：warning 通胀）；注入行补 md 资产全名例
- 0.8（2026-09-13）全名定义入注入行与 Structure（test-repo 走查发现：约定原只活在附检源码，零先验必猜错）
- 0.7（2026-09-13）注入源移交 manifest：删 Checks / Inject / Attachments 节，md 回归纯文档
- 0.6（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.5（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.4（2026-09-11）机械项收编附检脚本：断链 / 乱码 / 孤儿 / 新增别名二义（error）与 related 单向（信息）；hub 榜留语义项
- 0.3（2026-09-10）断链降级 warning（尚未写下的知识，非畸形）；孤儿判定作用域明文（派生页不算入链源）
- 0.2（2026-09-10）manifest 增 layer: field（分层立设：字段层，零依赖）
- 0.1（2026-09-09）新立：链接语法与 related / aliases 字段；断链检查自原 lint 转化，孤儿检查自 notes 移交
