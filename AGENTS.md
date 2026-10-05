# Project Intro

This repository (directory `agent-obsidian-template`, working name **vault-wiki**) is the build project of the vault-wiki framework and also its first **prototype instance**: since 2026-09-08 the "plugin + command" architecture has landed directly, with spec docs distilled afterwards. **Positioned as a team project** (converted from personal use on 2026-10-02; universalization and matrix testing deferred — fix as used).

- Layout: `.meta/` (prototype core: plugin & command masters, protocol artifacts, mechanical scripts, human docs `docs/`) · `wiki/` (the inner side of the inner/outer divide) + `vault/` / `projects/` / `cuhksz/` (external domain containers, data areas — cuhksz/ school domain: bb/ course workspace + registry/ regulation materialization) · `.agents/skills/` (deployment copies) · `connectors/` (connector masters: deployment-side CLI factual interface + skill usage disclosure — `connectors/*/SKILL.md` lands in `.agents/skills/` via kernel deploy; currently bb-cli / sis-cli / mail-cli / bili-cli) · `test-repo/` (**independent test sandbox**: whitelist-tracked — only the `.meta/` and `.agents/` framework mirrors are committed and re-copied on root-side sync; experimental content inside the sandbox stays local, never in history; the sandbox does not perceive this project)
- Terms: **wiki** = the md world, the inner side of the inner/outer divide (per-domain projections + native notes); **domain** = the adapter contract for an information source outside the wiki (vault is the default domain; lark / project / email / bb / bili are domains too); **vault** = the default domain — the real-asset repository (command side append-only; deletion & editing are the human's freedom)
- Conflict adjudication: the prototype's current state and converged discussion conclusions prevail; spec distillation merges historical versions under `.meta/docs/`
- The personal library (`D:\Obsidian repo\agent-obsidian`) is a read-only reference sample: the original wiki idea has been transformed into this prototype (see log 2026-09-08)

# Core Principles

1. **Prototype first, docs later**: once a design converges in discussion it lands directly as a prototype (`.meta/` plugins & commands) and is validated by real operation; spec docs are distilled afterwards from what actually runs — never drafted in advance.
2. **Skeleton vs instance separation**: anything personal (journal systems, material preferences, address rules…) is recorded as instance configuration, never architecture. Touchstone: what cannot move into a brand-new instance is personal-layer leakage into architecture; likewise, **whatever the agent is assumed to know (unstated conventions, format priors) is knowledge-layer leakage** — in real deployments the agent learns only via the SASU-L order (system prompt → AGENTS.md → Skills → user's words → loop), zero priors.
3. **The architecture does not enumerate**: no enumeration of file formats or note types (a type is a frontmatter field); structure is specified by each plugin; the wiki directory splits into the proxy layer (`wiki/vault/`) and the native area (`wiki/notes/` notes, `wiki/sessions/` sessions).
4. **No tool-private formats**: md + plain files are the foundation; Obsidian, WebUI etc. are replaceable viewers.
5. Actively maintain `log.md` and `README.md`: log holds project status, stages & progress, next steps, past operations — total under 2.5k chars, operations dated (to the day); proactively consolidate when stale or overlong (**consolidation requires prior user consent**); README is the outward charter digest — after structural changes (positioning / layout / plugin & command counts / collaboration rules) land, refresh the affected paragraphs; fix staleness on sight — the authoritative source is always this file. **Team-mode addendum (2026-10-02)**: members **append-only, never edit or consolidate** the log at runtime; over-limit does not block and is not privately consolidated — it flows with the branch and the current user notifies the owner; consolidation rights & consent belong to the owner.
6. This file is directive; total length <250 lines (widened 2026-10-01, originally 150); details go behind pointers; read the important pointers proactively at the start of every session.
7. Project docs and disclosures are written in English (switched 2026-10-06 from Chinese-first; historical Chinese log entries are preserved as-is — the log switches language append-only, see its note); structure files keep ASCII names.
8. **Small proactive commits**: once a design is finalized or a skeleton change lands, the agent commits proactively without waiting for user instruction (anti zero-commit trap); commit message format `module: summary` (e.g. `skeleton: minimal set and directory layout finalized`); one commit does one thing; no proactive push (routine pushes within the entrusted manager's duties excepted — see the delegation clause under "User Requirements"); history-rewriting operations forbidden.
9. **Complete disclosure, validate by use**: skills and specs are written per the SASU-L disclosure paradigm (zero priors — see principle 2 and `.meta/protocol/experiments.md`); framework changes are judged by real-use feedback, fixed as used — no matrix testing (ruled 2026-09-12).
10. **Analysis rounds must not execute**: when the user's request is a brief / discussion / assessment / proposal ("summarize the current state", "any objections", "take a look"), the round delivers analysis only and touches no file; execution waits for an explicit verb (execute / land / do / merge / push…). Preference statements ("names should be sensible", "should be added") are requirement input, not authorization; when an utterance contains both, the request verb prevails; when ambiguous, ask first (ruled 2026-10-01, after a brief-round overstepped into renaming).
11. **Global vs domain plugins**: two classes — global plugins (cross-cutting services & sinks, e.g. trust / log / todo / calendar / notes / user-profile) and domain plugins (domain instance families; whichever depends on domain directly is a domain base, the rest belong via transitivity). Global plugins may declare **bridges** — the manifest `bridge` key marks the attach cardinality (mandatory | on-demand), with integration format & details in the PLUGIN.md bridge section; domain plugins attach bridges via depends, and **mandatory bridges are verified complete by kernel validate** (missing edge on a domain base → error). A bridge holds only "who is here, how to integrate" — no domain-shape knowledge (each plugin owns its own disclosure, SASU-L) (ruled 2026-10-02, derived from the group meeting).

# Commands (user-triggered)

- **init**: read this file's pointers and `log.md`, align across sessions; judge whether the log needs consolidation and pointers need updating.
- **update**: update `log.md` and related docs, then git commit; append a briefing: what was done this round, key decisions & rationale, impact.
- **discuss**: discuss and align professionally and concisely; discussion only — destructive operations forbidden.
- **recover**: end a special state (e.g. discuss) and resume normal work.

# User Requirements (hard constraints)

- The personal library `D:\Obsidian repo\agent-obsidian` is read-only to this project; any backfill requires explicit user instruction.
- Personal private content (user profiles, journals, personal records) must not be written into this repository — the framework is a universal artifact.
- Reference projects (`D:\My Programs\erp - ksbgs`, `D:\My Programs\aijia`) are pattern references only; modify nothing in them.
- **Commit boundary (everyone)**: only development artifacts enter git — `.meta/` (incl. `docs/`), `connectors/`, root-level charters, root data-container empty seeds (`cuhksz/`), test-repo whitelist mirrors (only `.meta/` and `.agents/`, re-copied on root-side sync — ruled by the owner 2026-10-04, fabricated examples stay out too). **Never committed**: real course/grade/submission data, personal privacy, credentials & sessions, sandbox experiment artifacts (everything outside the test-repo whitelist). `test-repo/` is an independent sandbox; its experimental content stays local; **once real experiments happen, none of its out-of-whitelist changes may be committed** — uploading any usage traces is forbidden (mirror updates go through root-side re-copy, never sandbox-side sync).
- **Git discipline (everyone)**: develop on branches; entering master requires the manager — **the manager is exercised by an agent on the owner's delegation (authorized 2026-10-02)**: branch review (red-line scan + kernel validate + projection convergence) → merge & push → remote branch governance (violations deleted on sight and reported to the owner) → PR-page operations (comment/review/close, leaving traces on GitHub — via gh CLI, credentials injected from the GH_TOKEN env var, token taken from `git credential fill`, never echoed or written to disk), with a log entry after each delegated action. One commit does one thing; self-check before merging that the diff contains no non-development content; **opening a gitignore whitelist or force-adding ignored instance data requires the repo owner's explicit authorization, recorded** (rule set after the 2026-10-02 member incident); history rewriting forbidden. **Reserved matters (never delegated; owner-explicit only)**: history rewriting, gitignore exemptions, deleting others' non-violating work, repository settings & member permissions, backup deletion.
- **Commit flow (everyone, standard)**: branch off the latest `master` (name = module-topic or feature/topic) → small commits (`module: summary`) → pre-completion self-check (`python .meta/scripts/wiki_plugin_kernel.py all` passes, diff free of non-development content, log append-only) → push the branch and **opening a PR is recommended** (GitHub merge-request page, the standard review channel, auto-closed with trace on merge; un-PR'd branches are reviewed & merged by the manager all the same) → manager reviews & merges, deletes the merged branch, logs and reports.
- **Collaboration alignment (everyone)**: before touching a plugin/connector, read `log.md` status & next steps; version numbers advance along the changelog — no skipping or pre-reserving; experiments & tests always land in the test-repo sandbox or locally, conclusions via conversation reports or `docs/`.

# Pointers

> Pointers are maintained proactively. Cross-session-critical pointers carry **ATTENTION**; volatile state (progress etc.) lives in `log.md`, never in this file.

- `log.md` — project log: status, stage, next steps, past operations **ATTENTION**
- `.meta/` — prototype core: structural plugins (`plugins/` — the two conceptual roots domain (outer · domain contract) and wiki (inner · origin dichotomy) + domain instance families: vault (default domain; mapping is its mapping law, structure manages its layout), lark (external domain base; pointer/archive dual form; in-domain lark-docs cloud-docs domain / lark-im interpersonal domain), project (self-standing container domain: projects/ workspace + wiki declaration page), email (personal mailbox domain: wiki/email/ account + three assets + unified digest, connector mail-cli), bili (bilibili content domain: wiki/bili/ identity page + digest + emergence-based UP & video archives (video page two sections: overwritable summary + append-only review), query-and-answer, watch-video degradation chain, connector bili-cli — low-risk write whitelist needs the user's explicit verb behind double gates), cuhksz (school domain base: identity page + subsystem family — bb course ops (bb/ workspace + wiki/cuhksz/bb/ territory, term/course dual-side isomorphism; bb-map is its mapping law, bb-track manages the cognition profile), sis student records (wiki/cuhksz/sis/, connector sis-cli), registry academic regulations (materialization + pointer index)) + notes/sessions/link/tag/trust/index/hot/log/user-profile/todo/language/device + calendar the time territory (lark-calendar as source adapter) + cron the time-automation territory (declaration-as-source, executor-as-projection; session|script forms) + tmp scratch area — no layering, injection order = dependency topology + alphabetical) plus command masters (`command/`), protocol artifacts (`protocol/`: field registry, action discipline, SASU-L disclosure paradigm) and mechanical scripts (`scripts/`: wiki_plugin_kernel install/compliance/inject/copy + pipeline derived-layer index/tags/hot/log/verify + wikilib the page-parsing backbone); the AGENTS.md injection region is their projection **ATTENTION**
- `wiki/`, `vault/`, `projects/`, `cuhksz/` — data-area skeletons (kept as empty seeds: content belongs to deployment instances, not accumulated in this project — live-repo validation goes through `test-repo/`); `.agents/skills/` — deployment copies of command & connector skills
- `.meta/docs/` — human docs (the authoritative mechanics live in the kernel reference skill; docs do not mirror mechanics): `intro.md` introduction (how we got here — narrative & lineage), `mechanics.md` mechanics (each mechanism one level deeper + a bb-family walkthrough), `usage.md` usage guide (three work loops), `quickstart.md` deployment walkthrough, `research-*.md` research files (user-profile selection, landscape benchmarking)
- `README.md` — project charter
- Design lineage (discussion records, read-only): personal library `wiki/meta/2026-08-25-wiki运行时重构决策.md`, `wiki/sessions/2026-08-25-wiki架构调研与docs-first重构设计.md`
- Reference projects: `D:\My Programs\erp - ksbgs` (source of the AGENTS.md pattern: charter + pointers, log capacity management, command set); `D:\My Programs\aijia` (wiki pointer-style references)

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:domain v0.1 -->
- 域抽象（外）：wiki 只认内外；外域 = 一份适配器契约（外领地 / 落地策略 / 身份证明 / wiki 侧属地 / 写模型 / 信任模型），各域插件自行声明、域内插件经传递属域；落地本质是写模型选择（终态资产→只增仓储、过程容器→全权读写、真相在别处→指针），投影密度随翻译成本（镜像 / 指针 / 仅披露）；借 vault 或指针为默认姿态，自立容器是例外（判据：写模型或结构刚性分叉）；域须在 wiki 内可发现（声明页或注入行）
<!-- /plugin:domain -->

<!-- plugin:wiki v0.7 -->
- wiki 容器 `wiki/`（内外之分的内侧）：出身二分——属地页两形：代理页（默认，可对账外源的投影，属地路径由各域注入行自披露）与域内原生页（域声明的域侧档案——真身在此、无外源对账，形态归域插件；首例 bb-track 认知档案 user.md）；属地之外其余为原生页（真身在此的写作物；会话页是纪要非镜像——对话消逝后页面即真身，写作即出生）；index / tags / hot / log 为派生页（机械投影）；页面 frontmatter 取最小 YAML 子集（顶层标量 / 块列表 / 一级块映射），更复杂结构不受解析
<!-- /plugin:wiki -->

<!-- plugin:device v0.2 -->
- 设备档案：个人设备一设备一页落 `wiki/notes/`（type: entity 形态建议，页名自由、同名尾缀消歧），frontmatter `device` 块映射登 serial / purchased / warranty_until（最小键集，余开放：model、vendor 等），正文 `## 工具环境` 摘要节记连接器/运行时/通道在场级信息（跨设备互查，装卸软件时同步；全量软件清单不记——现查即得）；发票照片类资产走 vault 物化、页面 wikilink 关联（跨件引用不立依赖）；trust 可选挂——人手登记即 human 证据、静态事实不挂 stale_after；到期提醒——附检扫 warranty_until，30 天内临期或已过期呈 warning 清单，经用户确认受托追加 todo 行（受托即追加，不自动写）；实时状态监控与团队借还不做（范围边界）
<!-- /plugin:device -->

<!-- plugin:hot v0.10 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条、<5 日、单条 ≤200 字），agent 进库先读此页；写前先淘汰越界
<!-- /plugin:hot -->

<!-- plugin:language v0.2 -->
- 行文声明页 `wiki/language.md`（type: language）：产出语言与行文基线——frontmatter `language` 块映射 = 规范键→一句话规则（开放词表；域件消费键先例：teaching 讲解（bb-teach）、annotation 解析（bb-quiz））+ `terms` 块映射 = 术语原文→统一译名，正文沉淀译法注记（只增）；agent 产出写作物落笔前先读此页，页面或缺席键 = 跟会话语言（对话用什么语言产出就用什么；专名、代码、路径、命令、文件名恒保留原文——语言中性纪律）；框架不预设具体语言，本页是默认基线非强制——域件源对齐纪律（如试题语言跟课程材料）优先；术语涌现制——无表术语首现括注原文、反复命中才登记，人直接编辑合法
<!-- /plugin:language -->

<!-- plugin:link v0.14 -->
- 链接语法 `[[页面全名]]`——全名 = wiki/ 内相对路径去末尾 .md（如 `notes/X`、pdf 资产代理 `vault/a.pdf`、md 资产代理 `vault/原名.md`，仅去一个）；禁截断式引用，同名歧义带路径；字段 `related` / `aliases`；断链 = warning（尚未写下），孤儿（无入链无引用，派生页不算源）= notes 知识页 warning、领地值登记页 info（动态读 registry type.values，除 session）
<!-- /plugin:link -->

<!-- plugin:log v0.15 -->
- 运行日志 `wiki/log.md`：置顶追加、条目不改写，条目 = 日期 + 类型（map/save/query/check/plugin/todo/profile/other）+ [域]（可缺省——无域事务；log 必依桥：域基座必依赖本件，宪法准则 11）+ 一句话；窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`
<!-- /plugin:log -->

<!-- plugin:notes v0.15 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识，细分靠 type 字段（形态词表开放，默认值见 registry）；不可再生区，命令只增不改；session 与 profile 型不落本区（归 sessions / user-profile 领地）；notes 按需桥——域件单向派生高价值结论涌现入本区、须回链来源页（宪法准则 11，格式归本桥）
<!-- /plugin:notes -->

<!-- plugin:sessions v0.9 -->
- 原生会话 `wiki/sessions/`：会话骨干页（type: session，participants 必填=actor 列表，默认命名 YYYY-MM-DD-<主题>）；高价值主题提升为 `wiki/notes/` 独立页并回链；不可再生区，命令只增不改
<!-- /plugin:sessions -->

<!-- plugin:tag v0.11 -->
- 页面 `tags` 字段：YAML 列表，主语言跟行文声明页 `wiki/language.md` 的 default 键（页面或缺席键跟会话语言）、英文 tag 小写 kebab-case，层级 ≤2（`/` 分隔），每页 ≤5；开放语义分类，禁止复述 type
<!-- /plugin:tag -->

<!-- plugin:tmp v0.1 -->
- 临时区 `wiki/tmp/`（路径即领地，type: tmp 可标可不标、落领地外 → error）：草稿与解析中间产物住所，无留存承诺随时可清理；对派生层隐身——不入 index/tags、不作链接源、断链豁免（草稿断链 = 尚未写下，转正时闭合）；珍贵草稿及时转正（save → notes / 并入 project 决策区），转正即删稿；解析产物随手设 stale_after，超龄由 check 报清单、处置经确认（不自动删）；敏感中间产物建议实例 gitignore 本目录
<!-- /plugin:tmp -->

<!-- plugin:trust v0.9 -->
- 信任字段（页面可选）：`generated`（谁生成）/ `verified`（事件列表，项单行 by+at）/ `stale_after`（过期时刻）/ `sources`（来源与信号）；层级推导不落盘——无记录=unverified、仅 agent/process=machine-confirmed、含 human=human-reviewed、过 stale_after=stale
<!-- /plugin:trust -->

<!-- plugin:calendar v0.2 -->
- 时间领地：声明页 `wiki/calendar.md`（`calendar` 块映射 = 源键→源声明，manual-only 可缺）+ 月页 `wiki/calendar/YYYY-MM.md`（两节制——`## 日程` 源投影整节重刷、`## 手记` 只增；事件行 `- MM-DD HH:MM~HH:MM 标题（源键）` 可带 wikilink，事件不建页）；未来滚动、过去冻结（月份走完不可改写）；月页 stale_after 默认 2 天；与 todo 边界——日历存何时有何事、todo 存何事待办，可单向派生；calendar 按需桥——域件单向派生带源键日程行入当月 `## 日程`（宪法准则 11，格式归本桥）
<!-- /plugin:calendar -->

<!-- plugin:cron v0.1 -->
- 时间自动化领地 `wiki/cron/`（周期自动化意图的家，每任务一页纯目录制——目录即声明全集）：任务页 type: cron + `cron` 块映射（schedule 节奏 / action 动作 / form 执行形态 session 会话版|script 脚本版 / domain 属域 / status active|paused|deprecated / last_run 最近运行机器维护 / machine 可选执行机锚）+ 正文两节（`## 任务` 动作详情与指针回链属域 skill；`## 运行纪要` 只增收敛——异常/修复/变更决策，正常运行不记，历史归 log）；**声明为源、执行机构为投影**（harness 可替换，宪法准则 4）——部署/换机重放：active 页逐条落执行侧，session 版在当前 harness 调度设施建任务（prompt 按 SASU-L 自包含：读任务页按页执行 + 失败 log 报告 + 不阻断他任务）、script 版生成系统任务条目（crontab 行/任务计划命令）**经用户确认写入系统**；对账进 check 附检——active 页集 ↔ harness 任务清单 ↔ 系统任务清单（尽力读）三方 diff 漂移 → warning、last_run 超节奏周期 → warning（声明在而投影丢失）；意图变更同步：人改 status 经确认后 agent 同步删/停执行侧任务（双向以声明页为真源）；**统一失败纪律**——失败源 log 报告（类型 other 标任务名）不阻断他任务，修复委托单向派生 todo；cron 按需桥——域件立定时任务时建任务页 + depends 挂本件（宪法准则 11，页骨架与登记/重放/对账纪律归本桥，任务动作形态归域）；边界三分——todo 一次性委托、calendar 事件事实（何时有何事）、cron 周期自动化意图（何时自动做什么），任务产出仍按各域纪律落位
<!-- /plugin:cron -->

<!-- plugin:cuhksz v0.2 -->
- CUHK-SZ 学校域 `wiki/cuhksz/`（外领地 = cuhk.edu.cn 学校系统族：bb.cuhk.edu.cn 课程运行 · sis.cuhk.edu.cn 学籍制度 · registry.cuhk.edu.cn 教务制度；统一认证 STS ADFS，连接器 bb-cli / sis-cli 纯只读）：域声明页 identity.md（type: cuhksz + sis 块映射学籍身份，**缺席即建**——数据源 sis-cli transcript）；域根只持身份与子系统导航，速写归各子域；子系统族（bb 五件 / sis / registry）经 depends 挂靠、经传递属域；域内互引免桥（宪法准则 11 同域直引）；个人官方 PDF（证明/成绩单）落 cuhksz/sis/ 域内物化——**域有自立容器则域内落地，vault 仅兜底无容器域**（2026-10-05 所有者裁定修正，弃 device 先例的借 vault 惯性）
<!-- /plugin:cuhksz -->

<!-- plugin:index v0.12 -->
- 索引溢出减负制：根 `wiki/index.md` 恒在（含 format_version——页面格式契约版本，不兼容变更时进位），直列全部可达页（本目录 + 未切子树，全路径 wikilink）；某索引清单超窗（≤25 条，参数以 pipeline 源码为准）时按子树页数降序切子目录自立 `index.md`（入口行带页数）——小库常为单索引，披露边界随内容质量浮现；`wiki/tags.md`（tag 反向索引）不变；只聚合、永不手编、纯函数重建、索引不发明结构（本级平铺超窗如实全列，解药是分子目录非改索引）；重建走 `pipeline.py index`，检索第二入口
<!-- /plugin:index -->

<!-- plugin:lark v0.4 -->
- 外部指针领地 `wiki/lark/<profile>/`（一企业一目录，目录名 = lark-cli --profile 名，agent 调用必带）：基座立 profile 抽象与身份页 `profile.md`（一句话 + TTL 覆写），域插件（lark-docs…）在任一 profile 下平行展开；指针页 type: lark + `lark` 块映射（profile/kind/token/url），token↔页一比一即身份证明；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（默认 7 天），用前查 stale、stale 即带 --profile 现拉刷新（agent 即同步器）；资源消失标 status: deprecated 不删；新 profile = 建目录 + 身份页，域插件自动覆盖；CLI 纪律：--profile 必带、auth 现查不落盘、入新域前 lark-cli skills read 先行；领地页面两形——指针页全可再生，档案页分区（frontmatter 机械区对账维护 + 正文沉淀区只增不改，形态归域插件）
<!-- /plugin:lark -->

<!-- plugin:project v0.4 -->
- 项目容器 `projects/<项目名>/`（工作区，agent 全权读写——与 vault 只增相对）：项目本体与跟踪全住文件夹，惯例自述 `project.md`（四区：目标与上下文 / 阶段（checkbox+日期）/ 任务（行不建页）/ 决策（只增）；stage 规划/进行/暂停/完成开放词表）；wiki 端仅声明页 `wiki/projects.md`（type: project，`projects` 块映射 = 项目名→一句话，与目录双向 diff，漂移同 structure）；涉及项目内容的检索直查 projects/ 子树；与 todo 边界——todo 是 agent 委托活工作集，project.md 任务是持久分解事实源
<!-- /plugin:project -->

<!-- plugin:todo v0.3 -->
- 临时记忆 `wiki/todo.md`（type: todo）：跨 session 委托与提醒，条目 = 触发条件（日期或情境）+ 一句话 + by/at；新 session 开始先读此页（先于 hot，缺席即建空页），日期已到或已过的条目主动提醒用户；受托即追加，完成即销账（`[x]` 并写 log 行——历史归 log），已结 ≤20 条超限静默清理，本页只留活工作集；todo 按需桥——域件单向派生行动项入本页（宪法准则 11，格式归本桥）
<!-- /plugin:todo -->

<!-- plugin:user-profile v0.4 -->
- 用户画像 `wiki/profile.md`（type: profile）：对使用者的持续认知档案，静态身份层 + 动态偏好层，维度不枚举；收敛式更新——新值取代旧值、正文留痕；断言必带证据 wikilink（wiki 内页面皆可：会话页、vault 代理页、lark 档案页），偏好层挂 stale_after；零自有字段复用 trust，不属 notes 领地，不打 tags（单页直接读取，不入词表检索）；更新走 profile 命令——双轨触发（用户明示 / agent 识别显著信号自发调用），首次触发即自建页面；个性化决策（称呼、风格、偏好）前先读此页；认知桥（按需，宪法准则 11）——域认知页经画像正文 `## 域认知` 节登记（行 = 域名 + 路径形 wikilink，如 bb-track user.md），画像只聚合指针不复制域状态，个性化输出前读画像及其登记认知页；桥只持「谁在、去哪读」，认知页形态归域插件
<!-- /plugin:user-profile -->

<!-- plugin:vault v0.6 -->
- 默认域——真实资产仓库 `vault/`，wiki 侧属地 `wiki/vault/`：容纳任意格式资产，兼作他域落地仓储（url 字段即借道接口）；命令侧只增，删改自由属于人；布局规约归 structure 插件
<!-- /plugin:vault -->

<!-- plugin:bb v0.9 -->
- 课程运行子域（cuhksz 域内）`wiki/cuhksz/bb/`（外领地 bb.cuhk.edu.cn，连接器 bb-cli 纯只读，用法与位置见 bbcli skill）：双侧同构 `<term>/<course>/`——外 `cuhksz/bb/` 课程工作区（机器拉取物：文档类全量物化、媒体类默认指针化、提交件 submissions/，只增；笔记保留子区 notes/——学习笔记住所，人为主、ai 产物共居（teach 讲解沉淀 ai 笔记平铺带 origin: ai、quiz 考卷住 testing/ 子区；ai 产物只增不覆写；删改自由属于人，fetch/对账/映射永不触碰人的笔记、读取合法）），内 `wiki/cuhksz/bb/` 属地，目录名 = 学期名/课程代码（如 2610UG/AIE3005），machine id 与学期状态落身份页 bb 块映射（term_id/course_id/term_status）作一比一身份证明，同期同代码尾缀消歧、停用标 status: deprecated 不删；域根速写页 inbox.md（近窗公告蒸馏 + 临近截止 + 未交提醒双源——作业无提交 ∪ 成绩册有 due 无 attempt，行标课程，整页可再生短 TTL，**缺席即建**；frontmatter 兼域配置——terms 块映射现役学期与冻结标记）；公告拆信不存档（作业变更→assessments、考试/政策/分组→info、行动项→todo、资源发布→fetch 即弃，原文现拉即得）；课件物化后即本地终态资产豁免 TTL；投影细则见 bb-map 插件；凭据会话只存本机不入库；课程/成绩/提交数据属实例数据不入框架仓库；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（默认 1 天，速写页覆写；日期粒度，过期判定以当日为限），agent 即同步器
<!-- /plugin:bb -->

<!-- plugin:bili v0.3 -->
- bilibili 内容域 `wiki/bili/`（外领地 bilibili.com web API，连接器 bili-cli——web cookie 登录态、只读为主，用法与命令面见 connectors/bili-cli/SKILL.md）：域声明页兼身份页 bili.md（type: bili + bili 块映射 mid/nickname/TTL 覆写 + watch 块映射关注源清单（UP 主名→mid+一句话），**缺席即建**——数据源 bili-cli me）；**查询即答不默认投影**——搜索/视频详情/字幕/收藏夹/历史/稍后再看现拉即答（公开端点免登录、个人数据需登录态，红线见 bili-cli skill），高价值结论涌现入 notes 回链；UP 主档案 up/ 涌现制（反复命中或用户明示才立档——机械区 mid 一比一 + 最新投稿快照 + stale_after 对账维护、沉淀区关注理由与相关结论只增收敛）；视频档案 video/ 明示制涌现（用户明示入库或反复查询命中才建，未入库视频 URL 即指针、引用走正文链接）——两区制 `## 摘要`（ai 产物 origin: ai 可再生成覆写，对固定源蒸馏）+ `## 评价`（human 证据只增，页升 human-reviewed）；**看视频降级链**（停于首中）：CC 字幕 → AI 字幕（需登录）→ 官方总结（需登录）→ 音频落 wiki/tmp/ 本地转写（经用户确认、用毕即弃）；速写页 inbox.md（近窗蒸馏：关注源新投稿 + 个人数据要点，行标来源，整页可再生短 TTL 默认 1 天，**缺席即建**；节奏两步走——现阶段会话内现拉触发，watch 清单与蒸馏格式经真实使用稳定后升 cron 任务页（form: script，digest 子命令预留，登记/重放纪律见 cron 插件））；**低危写白名单**（稍后再看增删/收藏夹增删/点赞，均须用户明示动词 + CLI --yes 双门）之外写操作永不提供（投币/评论/转发/关注/私信/弹幕，raw 亦不承载）；单向派生只出不回：直播/首播等明确时间点 → calendar 日程行、行动项 → todo、高价值结论 → notes（回链属地页）——todo/calendar/notes 三桥；cookie 凭据只存本机不入库、观看历史/收藏夹属实例数据不入框架仓库；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（日期粒度，身份页覆写），agent 即同步器
<!-- /plugin:bili -->

<!-- plugin:email v0.4 -->
- 个人邮箱域 `wiki/email/`（一账户一目录，agent 调用必带账户）：域根统一速写 `inbox.md`（近窗蒸馏、行标账户、整页可再生、短 TTL）+ 全局人档 `people/`（token = 邮箱地址，跨账户一人一页——token 作用域决定家；aliases 收多地址同人，正文与我的关系只增收敛）；账户目录——身份页 `account.md`（地址/协议/拉取窗口/TTL 覆写/涌现条件/关心区声明）、线程档 `threads/`（机械区 Message-ID 成员列表 + 沉淀区议题结论只增，快照节冷源可全文）、源档 `sources/`（订阅治理：类型/节奏/阅读信号/处置策略）；全量映射禁止——检索现拉即弃，反复命中才立档（涌现制）；单向派生只出不回——行动项→todo、邀请→calendar、附件→vault 物化、高价值→notes（回链线程档）；agent 对邮箱只读（PEEK 不标已读、不移动不删除），发送类操作永远须用户明示；资源消失标 status: deprecated 不删；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（默认 1 天，身份页覆写），agent 即同步器
<!-- /plugin:email -->

<!-- plugin:lark-calendar v0.2 -->
- lark 日历源（calendar 首个适配器）：声明页 `calendar` 块映射值 = `lark/<profile> <calendar_id|primary>`（profile 须为 wiki/lark/ 现役目录）；拉取 `lark-cli --profile <名> calendar …`（instance_view 当月/下月窗口）；只写月页 `## 日程` 节、行尾标源键；不碰手记节与已冻结月页；日更节奏 = 经 cron 桥登记任务页（form: session，登记/重放/对账纪律见 cron 插件，失败源 log 报告不阻断他源）
<!-- /plugin:lark-calendar -->

<!-- plugin:lark-docs v0.1 -->
- 云文档域（服务 profile 抽象）：每 profile 枢纽页 `<profile>/docs.md`（kind: docs）——frontmatter `docs` 块映射 = 关心区→范围一句话（实例配置），正文「云盘结构速写」（蒸馏非镜像，stale_after 管）；指针页落 `<profile>/docs/<关心区>/`，kind 跟 lark obj_type（docx/wiki/sheet/base/file…开放词表）；全量映射禁止——枚举只服务速写与关心区解析；快照节 `## 快照 YYYY-MM-DD` 选段追加、禁全文复制；TTL 默认 7 天（profile.md 覆写）
<!-- /plugin:lark-docs -->

<!-- plugin:lark-im v0.1 -->
- 人际域（档案页，基座分区制）：枢纽 `<profile>/im.md`（`im` 块映射 = 策略：群同步 / 涌现 / 关注 / 排除）；群档 `<profile>/im/chats/`（kind: chat——`description` 群功能 + `key_members` 关键人 wikilink，正文沉淀区 = 议题记录 `## 日期 议题→结果` 只增、按需拉窗蒸馏经确认追加）；人档 `<profile>/im/people/`（kind: person，token = open_id，department/position 由 contact 解析，chat_id 为 p2p 锚，正文沉淀区 = 与我的关系，只增收敛）；人档涌现制（p2p / 点名 / 高频，条件写枢纽）——不建全量通讯录（contact 只解析不遍历）；群参与人只存关键不存全员；文件名清洗 + 重名 token 尾缀；发送类写操作永远须用户明示；隐私红线：主观关系内容不入框架仓库与 test-repo；trust lazy-refresh 同基座
<!-- /plugin:lark-im -->

<!-- plugin:mapping v0.8 -->
- 代理层 `wiki/vault/`：与根 `vault/` 1:1 镜像（代理名 = 原名 + .md），页面必有 raw_file / raw_sha256；路径即出身证明
<!-- /plugin:mapping -->

<!-- plugin:registry v0.1 -->
- 教务制度子域（外源 registry.cuhk.edu.cn 教务处官网，**无连接器**——人工下载经用户明示、半自动物化）：物化区 `cuhksz/registry/`（官网 PDF 只增，版本批次进位不覆写）+ 属地 `wiki/cuhksz/registry/`——索引页 schemes.md（全校学院→专业→方案页 URL 指针；建页源：本科专业清单 registry.cuhk.edu.cn/page/20 与本科生手册 /page/22 族，含双主修/联合课程/副修；人机共维护、公开制度导航）与代理页（raw_file/raw_sha256 + 要点蒸馏只增 + 版本对版记录）；**对版节奏** = 学期初与 Senate 公文日人工核对（页面无日期，以 PDF Last-Modified 抽查）；制度对照双源——本区规则 PDF 为制度源、sis-cli 学位进度报告（DPR）为动态源，对照结论涌现入 notes 回链；trust human-reviewed（人工核对）+ 版本锚，无 TTL（制度变更靠对版不靠过期）；停招专业（如电子信息工程 2015-2021）如实标注不删
<!-- /plugin:registry -->

<!-- plugin:sis v0.2 -->
- 学籍制度子域 `wiki/cuhksz/sis/`（外源 sis.cuhk.edu.cn，Oracle PeopleSoft CS，连接器 sis-cli 纯只读，用法与命令面见 connectors/sis-cli/SKILL.md）：速写页 inbox.md（近窗蒸馏——本学期课表概要/注册窗口/holds/最新成绩快照，行标学期，整页可再生短 TTL 默认 1 天，**缺席即建**）；**查询即答不默认投影**——成绩/历史/课表/考试现拉即答（term 交互与只读红线见 sis-cli skill），高价值结论涌现入 notes 回链；单向派生只出不回：注册窗口临期 → todo、课表/考试安排 → calendar 日程行（补 bb 挂缺的课表源）、学期成绩（终态事实）→ bb-track 证据流（域内直引免桥，经用户确认）；个人官方 PDF（在读证明/非官方成绩单）经用户明示下载落 `cuhksz/sis/` 域内物化 + 属地代理页（域有自立容器则域内落地，vault 仅兜底无容器域）；官方成绩单申请等写操作**永不入本域**（真实学籍后果）；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（日期粒度），agent 即同步器
<!-- /plugin:sis -->

<!-- plugin:structure v0.3 -->
- vault 结构声明 `wiki/structure.md`（type: structure）：frontmatter `structure` 块映射 = 目录→一句话语义，正文写预设（日期/格式/类型/混合，可嵌套）与说明；agent 放置资产先读此页按位落放；页面缺席 = 平铺容忍；人调整 vault 后同步声明，check 机械 diff（未声明的顶层目录 / 声明不存在的目录 → warning）
<!-- /plugin:structure -->

<!-- plugin:bb-map v0.15 -->
- bb 映射法则：属地 wiki/cuhksz/bb/<term>/<course>/ 规范形四桶（bb/ 保源形，桶名 v0.4 终裁：courseware/assessments/attachments；课程根另容 user.md 认知档案——bb-track 域内原生页，不受四桶约束）——info.md 课程信息页兼身份页（bb 块映射 term_id/course_id/term_status + 大纲课程政策类要点蒸馏（开放词表：评分/考核/师资/TA/分组/教学语言/AI 政策，info-N 锚点，缺项标未提供）+ 备注沉淀；存「何时有何事」，被评分事务全要素归 assessments）；courseware/ 知识点页每内容单元一份（单元 = bb/ 目录「讲义+附属文件合一」或扁平单文件，平行同类目录合为一页；知识点摘要（sm-N 锚点 + 一行概括 + 章节提示）+ 专有名词对照表 + 单元文件清单（清单即对应关系）+ raw_path 指针（未下载单元可缺省）；纯代理）；assessments/ 聚合页每作业/考试一页（汇总列 Weighted Total/Total 排除；四要素：要求/参考蒸馏（req-N/ref-N 锚点）/提交/结果机械快照，due 缺省不告警、无提交独立话术；assessment 块映射 due/submitted_at/score/status/column_id + raw 块映射角色→bb/ 路径 + `## 复盘` 沉淀只增）；attachments/ 1:1 代理平铺（raw_file/raw_sha256，纯代理）；落位判据——有成绩册列或提交动作→assessments/（汇总列与分节登记列除外——分节登记列 = 非知识考核的分节/出勤登记，如 Tutorial Section）、老师非讲义资产→attachments/、内容单元→courseware/、结构事实入 info.md；讲义/附件边界：随周次内容→courseware、支撑性资源→attachments；info 与 assessments 两形分区（机械区可再生覆写+沉淀区只增，重建不得触碰），courseware/attachments 纯代理（珍贵内容入 notes）；映射不改 bb/ 源侧、不复制原文全文、源消失标 deprecated 不删；API 快照节挂 stale_after=拉取日+TTL，本地对账代理无 TTL
<!-- /plugin:bb-map -->

<!-- plugin:bb-track v0.6 -->
- bb 认知档案：每课课程根 user.md（属地域内原生页首例，wiki v0.7 两形）——`## 认知读数` 收敛覆写（锚 courseware sm-N，粗粒度自陈合法，状态词开放；含目标层：课程目标 + 短期优先带时效）+ `## 证据流` 只增（日期+出处+断言+回链）；信号权重 human>machine>ai 笔记（弱证据，人复核升权）；应知不存（差距现算）、错题题级归 assessments 复盘、统计现算；更新双轨（agent 显著信号自发/用户明示），建档懒惰式；采集通道（bb v0.7 共居）——teach 显著答疑落 notes/ ai 笔记（弱证据）、quiz 自测判分落 notes/testing/（machine 证据），入流经用户确认、用法投影挂 bb-track 命令；学期即边界随 term_status 冻结；trust 天花板 machine-confirmed（含 human 证据升 human-reviewed），stale_after 默认 14 天可覆写；笔记区 notes/ 只读，可选属性 origin/form/stage（stage 标记属人）；认知经 user-profile 桥登记——建档时画像在场则维护其 `## 域认知` 节一行（bb + 路径形），缺席跳过不代建
<!-- /plugin:bb-track -->

<!-- plugin:bb-quiz v0.6 -->
- 出题自测 bb-quiz（bb-track 的 testing 消费侧）：用户指定范围 + 可选样例 → 生成试题（题型与难度中值对齐样例，无样例回落已知作业、再回落用户习惯；题干语言源对齐——跟样例/已知作业/课程材料）+ 解析（语言读者对齐——取行文声明页 `wiki/language.md` 的 annotation 键，页面或缺席键跟会话语言；每题标知识点 sm-N 位置）；知识点全集 = courseware sm-N、范围 = 用户指定子集、不越界（除非用户明示）；选题与难度分布参照 bb-track 熟练度/目标层/错题（stale 保守档、冷启动全场未锚点均匀出题），教学纪要（notes/ ai 笔记）best-effort 按需读；考卷落 cuhksz/bb/<term>/<course>/notes/testing/<名>-试题.md + -答案.md（origin: ai，只增）；判分（作答后）= 答案页追记 `## 判分` + 经确认回写 user.md 证据流（machine 自测）；写后 log 行（other --domain bb）+ verify
<!-- /plugin:bb-quiz -->

<!-- plugin:bb-teach v0.6 -->
- 教学消费侧 bb-teach（bb-track 的 teaching 消费侧）：提问即讲解——问题定位 courseware sm-N（query 检索 + bb-map 收窄）→ 读 bb-track 认知档案（读数/证据/目标，stale 先核对、未核对前保守档）→ 按熟练度×难度二维伸缩讲解（已知略讲/反问、未知讲透）+ 讲解语言读者对齐（取行文声明页 `wiki/language.md` 的 teaching 键，页面或缺席键跟会话语言）+ 术语先用户已锚点集、缺省查 language 页全局 terms 表兜底（冲突锚点集优先）+ 错题/目标注入 + 锚点回链；三层反馈闭环——单轮反馈不落盘、显著答疑沉淀 ai 笔记落 notes/（origin: ai 弱证据，一篇一问回链锚点）、仅显著信号（跨会话稳定/主动应用/machine 验证）才经确认收敛 user.md（写回委托 bb-track 契约）；讲解对话不写 log、笔记落盘与认知收敛走写后管道；档案缺席（冷启动）全场按未锚点讲、不拒答
<!-- /plugin:bb-teach -->

<!-- wiki-inject:end -->
