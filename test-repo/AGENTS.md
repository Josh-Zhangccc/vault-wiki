# test-repo

个人知识库：vault 收纳真实资产，wiki 做 md 代理与原生笔记，agent 零先验读写。md + 纯文件是底座，Obsidian 等仅为可替换 viewer；结构契约见下方注入区，库操作走命令。

## 布局

- `vault/` — 真实资产仓库（任意格式；命令侧只增，删改自由属于人）
- `wiki/` — md 代理层与原生笔记；hot / index / tags / log 为派生层，机械维护
- `.meta/` — 插件与命令主本、协议工件（registry / actions）、机械脚本（wiki_plugin_kernel / pipeline）
- `.agents/skills/` — 命令部署副本

## 运行纪律

- 进库先读 `wiki/hot.md`；检索走 `wiki/index.md` 与 `wiki/tags.md`
- 库操作走命令（map / save / query / check / plugin / wiki_plugin_kernel），流程见 `.agents/skills/`
- 不可再生区只增不改：vault/ 与 wiki/notes/、wiki/sessions/ 的删改自由属于人
- git 提交随库操作即做（`map: <资产名>` / `保存: <页标题>` 等，见 `.meta/protocol/actions.md`），不攒批

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:hot v0.9 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条、<5 日、单条 ≤200 字），agent 进库先读此页；写前先淘汰越界
<!-- /plugin:hot -->

<!-- plugin:link v0.9 -->
- 链接语法 `[[页面全名]]`——全名 = wiki/ 内相对路径去末尾 .md（如 `notes/X`、pdf 资产代理 `vault/a.pdf`、md 资产代理 `vault/原名.md`，仅去一个）；禁截断式引用，同名歧义带路径；字段 `related` / `aliases`；断链 = warning（尚未写下），孤儿（无入链无引用，派生页不算源）= 原生页 warning、代理页 info
<!-- /plugin:link -->

<!-- plugin:log v0.11 -->
- 运行日志 `wiki/log.md`：置顶追加、条目不改写，条目 = 日期 + 类型（map/save/query/check/plugin/other）+ 一句话；窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`
<!-- /plugin:log -->

<!-- plugin:notes v0.12 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识（概念/问答/决策/实体），细分靠 type 字段；不可再生区，命令只增不改；会话骨干页归 sessions 插件
<!-- /plugin:notes -->

<!-- plugin:sessions v0.8 -->
- 原生会话 `wiki/sessions/`：会话骨干页（type: session，participants 必填=actor 列表，默认命名 YYYY-MM-DD-<主题>）；高价值主题提升为 `wiki/notes/` 独立页并回链；不可再生区，命令只增不改
<!-- /plugin:sessions -->

<!-- plugin:tag v0.9 -->
- 页面 `tags` 字段：YAML 列表，中文为主、英文专名小写 kebab-case，层级 `父/子` ≤2，每页 ≤5；开放语义分类，禁止复述 type
<!-- /plugin:tag -->

<!-- plugin:trust v0.7 -->
- 信任字段（页面可选）：`generated`（谁生成）/ `verified`（事件列表，项单行 by+at）/ `stale_after`（过期时刻）/ `sources`（来源与信号）；层级推导不落盘——无记录=unverified、仅 agent/process=machine-confirmed、含 human=human-reviewed、过 stale_after=stale
<!-- /plugin:trust -->

<!-- plugin:vault v0.3 -->
- 真实资产仓库 `vault/`：容纳任意格式资产；命令侧只增，删改自由属于人
<!-- /plugin:vault -->

<!-- plugin:wiki v0.4 -->
- wiki 容器 `wiki/`：出身二分——`wiki/vault/` 下为代理页（有 vault 对应物），其余为原生页（出身在 wiki）；index / tags / hot / log 为派生页（机械投影）；页面 frontmatter 取最小 YAML 子集（顶层标量 / 块列表 / 一级块映射），更复杂结构不受解析
<!-- /plugin:wiki -->

<!-- plugin:index v0.9 -->
- 索引 `wiki/index.md`（根，含 format_version——页面格式契约版本，不兼容变更时进位）与各目录 `index.md`（渐进披露，逐层下钻）/ `wiki/tags.md`（tag 反向索引）：只聚合、永不手编，重建走 `pipeline.py index`，检索第二入口
<!-- /plugin:index -->

<!-- plugin:mapping v0.6 -->
- 代理层 `wiki/vault/`：与根 `vault/` 1:1 镜像（代理名 = 原名 + .md），页面必有 raw_file / raw_sha256；路径即出身证明
<!-- /plugin:mapping -->

<!-- wiki-inject:end -->
