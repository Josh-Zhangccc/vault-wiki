# test-repo

vault-wiki 参考实例：本目录是框架的部署彩排产物——additive 拷贝 `.meta/` 与 `.agents/skills/`、移植 wiki 骨架种子、实例侧 AGENTS.md 外壳的第一次实体化。库内数据为样例，可随时重置。

## 布局

- `vault/` — 真实资产仓库（命令侧只增，删改自由属于人）
- `wiki/` — md 代理层与原生笔记（结构契约见下方注入区）
- `.meta/` — 插件与命令主本（本实例持有拷贝）
- `.agents/skills/` — 命令部署副本

## 运行纪律

- 进库先读 `wiki/hot.md`；检索走 `wiki/index.md` 与 `wiki/tags.md`
- 库操作走命令（map / save / query / check / plugin / wiki_plugin_kernel），流程见 `.agents/skills/`
- 框架升级传播：根仓库框架变更落地后，本实例重拷 `.meta/` 与 `.agents/skills/`，重跑 `python .meta/scripts/wiki_plugin_kernel.py all`

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:hot v0.9 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条、<5 日、单条 ≤200 字），agent 进库先读此页；写前先淘汰越界
<!-- /plugin:hot -->

<!-- plugin:link v0.8 -->
- 链接语法 `[[页面全名]]`——全名 = wiki/ 内相对路径去末尾 .md（如 `notes/X`、pdf 资产代理 `vault/a.pdf`）；禁截断式引用，同名歧义带路径；字段 `related` / `aliases`；断链 = warning（尚未写下），孤儿（无入链无引用，派生页不算源）= warning
<!-- /plugin:link -->

<!-- plugin:log v0.11 -->
- 运行日志 `wiki/log.md`：置顶追加、条目不改写，条目 = 日期 + 类型（map/save/query/check/plugin/other）+ 一句话；窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`
<!-- /plugin:log -->

<!-- plugin:notes v0.11 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识（概念/问答/决策/实体），细分靠 type 字段；不可再生区，命令只增不改；会话骨干页归 sessions 插件
<!-- /plugin:notes -->

<!-- plugin:sessions v0.8 -->
- 原生会话 `wiki/sessions/`：会话骨干页（type: session，participants 必填=actor 列表，默认命名 YYYY-MM-DD-<主题>）；高价值主题提升为 `wiki/notes/` 独立页并回链；不可再生区，命令只增不改
<!-- /plugin:sessions -->

<!-- plugin:tag v0.8 -->
- 页面 `tags` 字段：YAML 列表，中文为主、英文专名小写 kebab-case，层级 `父/子` ≤2，每页 ≤5；开放语义分类，禁止复述 type
<!-- /plugin:tag -->

<!-- plugin:trust v0.6 -->
- 信任字段（页面可选）：`generated`（谁生成）/ `verified`（事件列表，项单行 by+at）/ `stale_after`（过期时刻）/ `sources`（来源与信号）；层级推导不落盘——无记录=unverified、仅 agent/process=machine-confirmed、含 human=human-reviewed、过 stale_after=stale
<!-- /plugin:trust -->

<!-- plugin:vault v0.3 -->
- 真实资产仓库 `vault/`：容纳任意格式资产；命令侧只增，删改自由属于人
<!-- /plugin:vault -->

<!-- plugin:wiki v0.3 -->
- wiki 容器 `wiki/`：出身二分——`wiki/vault/` 下为代理页（有 vault 对应物），其余为原生页（出身在 wiki）；index / tags / hot / log 为派生页（机械投影）
<!-- /plugin:wiki -->

<!-- plugin:index v0.8 -->
- 索引 `wiki/index.md`（根，含 format_version）与各目录 `index.md`（渐进披露，逐层下钻）/ `wiki/tags.md`（tag 反向索引）：只聚合、永不手编，重建走 `pipeline.py index`，检索第二入口
<!-- /plugin:index -->

<!-- plugin:mapping v0.5 -->
- 代理层 `wiki/vault/`：与根 `vault/` 1:1 镜像（代理名 = 原名 + .md），页面必有 raw_file / raw_sha256；路径即出身证明
<!-- /plugin:mapping -->

<!-- wiki-inject:end -->
