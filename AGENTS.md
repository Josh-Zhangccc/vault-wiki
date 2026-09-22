# 项目介绍

本仓库（目录 `agent-obsidian-template`，工程暂名 **vault-wiki**）是 vault-wiki 框架的构建工程，兼第一个**原型实例**：2026-09-08 起「插件 + 命令」架构直接落地，规范文档后置蒸馏。**定位个人自用**（2026-09-12 裁定：普世化与矩阵化测试搁置，边用边改）。

- 布局：`.meta/`（插件与命令主本，原型核心）· `wiki/` + `vault/`（数据区）· `.agents/skills/`（部署副本）· `test-repo/`（参考实例：自足虚拟库，内部不感知本工程；框架变更由根侧同步重拷）· `docs/`（设计档案）
- 术语：**wiki** = vault 的 md 代理层与原生笔记；**vault** = 真实资产仓库（命令侧只增，删改自由属于人）
- 冲突裁决：以原型现状与讨论收敛结论为准；规范蒸馏时归并 `docs/` 历史版本
- 个人库（`D:\Obsidian repo\agent-obsidian`）为只读实证样本：原 wiki 思想已转化为本原型（见 log 2026-09-08）

# 核心准则

1. **原型先行、doc 后置**：设计经讨论收敛后直接落地为原型（`.meta/` 插件与命令），以真实操作验证；规范文档事后从跑通的现实蒸馏，不预先立稿。
2. **骨架与实例分离**：个人化的东西（日记体系、素材偏好、称呼规则……）一律记为实例配置项，不进架构。试金石：搬不进一个全新实例的，就是个人层漏进了架构；同理，**假定 agent 已知的（未写明的惯例、格式先验）就是知识层漏进架构**——真实部署中 agent 仅按 SASU-L 顺序（system prompt → AGENTS.md → Skills → 用户原话 → loop）获知信息，零先验。
3. **架构不枚举**：不枚举文件格式与笔记类型（类型是 frontmatter 字段）；结构由插件各自规范，wiki 目录分代理层（`wiki/vault/`）与原生区（`wiki/notes/` 笔记、`wiki/sessions/` 会话）。
4. **无工具私有格式**：md + 纯文件是底座；Obsidian、WebUI 等都是可替换 viewer。
5. 主动维护 `log.md`：含项目现状、阶段与进度、下一步计划、过往操作；总量不超过 2k 字；操作标注日期（精确到天）；描述过时或过长时主动整合压缩，**整合须先征得用户同意**。
6. 本文件为指导性文件，总长度 <150 行；详细信息用指针引用；每个 session 开始时主动读取重要指针。
7. 产出文档以中文为主，结构文件用 ASCII 文件名。
8. **小步主动提交**：设计定稿或骨架变更落地后，agent 主动 git commit，不等用户指令（防零提交陷阱）；提交信息格式 `模块: 概述`（如 `骨架: 定稿最小集与目录结构`），一次提交只做一件事；不主动 push；禁止改写历史的操作。
9. **披露完备、以用代验**：skill 与规范按 SASU-L 披露范式写清（零先验，见准则 2 与 `.meta/protocol/experiments.md`）；框架改动以真实使用反馈为准、边用边改，不做矩阵化测试（2026-09-12 裁定）。

# 指令（用户触发）

- **init**：读取本文件指针与 `log.md`，跨 session 对齐；判断 log 是否需整合、指针是否需更新。
- **update**：更新 `log.md` 与相关文档并 git 提交；随后附简报：本轮做了什么、关键决策与理由、影响。
- **discuss**：以专业、简明的方式讨论对齐；只讨论，禁止执行破坏性操作。
- **recover**：结束特殊状态（如 discuss），恢复正常工作。

# 用户要求（硬性约束）

- 个人库 `D:\Obsidian repo\agent-obsidian` 对本工程只读；任何回填动作须用户明确指令。
- 个人隐私内容（用户档案、日记、个人记录）不得写入本仓库——框架是普世产出。
- 参考工程（`D:\My Programs\erp - ksbgs`、`D:\My Programs\aijia`）仅作模式参考，不修改其中任何内容。

# 指针

> 指针需主动更新。跨 session 的重要指针标注 **ATTENTION**；易变状态（进度等）放 `log.md`，不写入本文件。

- `log.md` — 项目日志：现状、阶段、下一步、过往操作 **ATTENTION**
- `.meta/` — 原型核心：结构插件（`plugins/`——概念双插件 wiki/vault + 桥接 mapping + notes/sessions/link/tag/trust/index/hot/log/user-profile/todo/structure + calendar 时间领地（lark-calendar 为源适配器）+ project 项目容器（projects/ 工作区 + wiki 声明页）+ tmp 临时区 + 外部指针族 lark（基座，指针/档案两形）与 lark-docs（云文档域）、lark-im（人际域），无分层，注入序=依赖拓扑+字母序）与命令主本（`command/`）与协议工件（`protocol/`：字段注册表、动作纪律、披露范式 SASU-L）与机械脚本（`scripts/`：wiki_plugin_kernel 装卸/合规/注入/副本 + pipeline 派生层管道 index/tags/hot/log/verify + wikilib 页面解析承重件）；AGENTS.md 注入区为其投影 **ATTENTION**
- `wiki/`、`vault/`、`projects/` — 数据区骨架（保持空种子：内容属部署实例，工程内不积累——跑库验证走 `test-repo/`）；`.agents/skills/` — 命令部署副本
- `docs/` — 设计文档（重开卷）：现行 `quickstart.md` 快速开始/部署走查、`pointers.md` 指针机制（信息披露挂载，架构核心概念）、`research-*.md` 调研档案（user-profile 画像选型、landscape 同类产品入库/出库对标）；历史档案 `00-principles.md`、`01-okf.md` v0.2 不起现行作用；现行规范以 `.meta/` 为源
- `README.md` — 项目章程
- 设计谱系（讨论记录，只读）：个人库 `wiki/meta/2026-08-25-wiki运行时重构决策.md`、`wiki/sessions/2026-08-25-wiki架构调研与docs-first重构设计.md`
- 参考工程：`D:\My Programs\erp - ksbgs`（AGENTS.md 模式来源：宪法+指针、log 容量管理、指令集）；`D:\My Programs\aijia`（wiki 指针化引用）

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:domain v0.1 -->
- 域抽象（外）：wiki 只认内外；外域 = 一份适配器契约（外领地 / 落地策略 / 身份证明 / wiki 侧属地 / 写模型 / 信任模型），各域插件自行声明、域内插件经传递属域；落地本质是写模型选择（终态资产→只增仓储、过程容器→全权读写、真相在别处→指针），投影密度随翻译成本（镜像 / 指针 / 仅披露）；借 vault 或指针为默认姿态，自立容器是例外（判据：写模型或结构刚性分叉）；域须在 wiki 内可发现（声明页或注入行）
<!-- /plugin:domain -->

<!-- plugin:hot v0.9 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条、<5 日、单条 ≤200 字），agent 进库先读此页；写前先淘汰越界
<!-- /plugin:hot -->

<!-- plugin:link v0.13 -->
- 链接语法 `[[页面全名]]`——全名 = wiki/ 内相对路径去末尾 .md（如 `notes/X`、pdf 资产代理 `vault/a.pdf`、md 资产代理 `vault/原名.md`，仅去一个）；禁截断式引用，同名歧义带路径；字段 `related` / `aliases`；断链 = warning（尚未写下），孤儿（无入链无引用，派生页不算源）= notes 知识页 warning、领地值登记页 info（动态读 registry type.values，除 session）
<!-- /plugin:link -->

<!-- plugin:log v0.12 -->
- 运行日志 `wiki/log.md`：置顶追加、条目不改写，条目 = 日期 + 类型（map/save/query/check/plugin/todo/other）+ 一句话；窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`
<!-- /plugin:log -->

<!-- plugin:notes v0.13 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识，细分靠 type 字段（形态词表开放，默认值见 registry）；不可再生区，命令只增不改；session 与 profile 型不落本区（归 sessions / user-profile 领地）
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

<!-- plugin:wiki v0.5 -->
- wiki 容器 `wiki/`（内外之分的内侧）：出身二分——各域声明属地之页为代理页（有域外对应物，属地路径由各域注入行自披露），其余为原生页（出身在 wiki）；index / tags / hot / log 为派生页（机械投影）；页面 frontmatter 取最小 YAML 子集（顶层标量 / 块列表 / 一级块映射），更复杂结构不受解析
<!-- /plugin:wiki -->

<!-- plugin:calendar v0.1 -->
- 时间领地：声明页 `wiki/calendar.md`（`calendar` 块映射 = 源键→源声明，manual-only 可缺）+ 月页 `wiki/calendar/YYYY-MM.md`（两节制——`## 日程` 源投影整节重刷、`## 手记` 只增；事件行 `- MM-DD HH:MM~HH:MM 标题（源键）` 可带 wikilink，事件不建页）；未来滚动、过去冻结（月份走完不可改写）；月页 stale_after 默认 2 天；与 todo 边界——日历存何时有何事、todo 存何事待办，可单向派生
<!-- /plugin:calendar -->

<!-- plugin:index v0.11 -->
- 索引溢出减负制：根 `wiki/index.md` 恒在（含 format_version——页面格式契约版本，不兼容变更时进位），直列全部可达页（本目录 + 未切子树，全路径 wikilink）；某索引清单超窗（≤25 条，参数以 pipeline 源码为准）时按子树页数降序切子目录自立 `index.md`（入口行带页数）——小库常为单索引，披露边界随内容质量浮现；`wiki/tags.md`（tag 反向索引）不变；只聚合、永不手编、纯函数重建、索引不发明结构（本级平铺超窗如实全列，解药是分子目录非改索引）；重建走 `pipeline.py index`，检索第二入口
<!-- /plugin:index -->

<!-- plugin:lark v0.3 -->
- 外部指针领地 `wiki/lark/<profile>/`（一企业一目录，目录名 = lark-cli --profile 名，agent 调用必带）：基座立 profile 抽象与身份页 `profile.md`（一句话 + TTL 覆写），域插件（lark-docs…）在任一 profile 下平行展开；指针页 type: lark + `lark` 块映射（profile/kind/token/url），token↔页一比一即身份证明；trust 天花板 machine-confirmed，stale_after = 拉取日 + TTL（默认 7 天），用前查 stale、stale 即带 --profile 现拉刷新（agent 即同步器）；资源消失标 status: deprecated 不删；新 profile = 建目录 + 身份页，域插件自动覆盖；CLI 纪律：--profile 必带、auth 现查不落盘、入新域前 lark-cli skills read 先行；领地页面两形——指针页全可再生，档案页分区（frontmatter 机械区对账维护 + 正文沉淀区只增不改，形态归域插件）
<!-- /plugin:lark -->

<!-- plugin:project v0.3 -->
- 项目容器 `projects/<项目名>/`（工作区，agent 全权读写——与 vault 只增相对）：项目本体与跟踪全住文件夹，惯例自述 `project.md`（四区：目标与上下文 / 阶段（checkbox+日期）/ 任务（行不建页）/ 决策（只增）；stage 规划/进行/暂停/完成开放词表）；wiki 端仅声明页 `wiki/projects.md`（type: project，`projects` 块映射 = 项目名→一句话，与目录双向 diff，漂移同 structure）；涉及项目内容的检索直查 projects/ 子树；与 todo 边界——todo 是 agent 委托活工作集，project.md 任务是持久分解事实源
<!-- /plugin:project -->

<!-- plugin:tmp v0.1 -->
- 临时区 `wiki/tmp/`（路径即领地，type: tmp 可标可不标、落领地外 → error）：草稿与解析中间产物住所，无留存承诺随时可清理；对派生层隐身——不入 index/tags、不作链接源、断链豁免（草稿断链 = 尚未写下，转正时闭合）；珍贵草稿及时转正（save → notes / 并入 project 决策区），转正即删稿；解析产物随手设 stale_after，超龄由 check 报清单、处置经确认（不自动删）；敏感中间产物建议实例 gitignore 本目录
<!-- /plugin:tmp -->

<!-- plugin:todo v0.1 -->
- 临时记忆 `wiki/todo.md`（type: todo）：跨 session 委托与提醒，条目 = 触发条件（日期或情境）+ 一句话 + by/at；新 session 开始先读此页（先于 hot），日期已到或已过的条目主动提醒用户；受托即追加，完成即销账（`[x]` 并写 log 行——历史归 log），已结 ≤20 条超限静默清理，本页只留活工作集
<!-- /plugin:todo -->

<!-- plugin:vault v0.5 -->
- 默认域——真实资产仓库 `vault/`，wiki 侧属地 `wiki/vault/`：容纳任意格式资产，兼作他域落地仓储（url 字段即借道接口）；命令侧只增，删改自由属于人；布局规约归 structure 插件
<!-- /plugin:vault -->

<!-- plugin:lark-calendar v0.1 -->
- lark 日历源（calendar 首个适配器）：声明页 `calendar` 块映射值 = `lark/<profile> <calendar_id|primary>`（profile 须为 wiki/lark/ 现役目录）；拉取 `lark-cli --profile <名> calendar …`（instance_view 当月/下月窗口）；只写月页 `## 日程` 节、行尾标源键；不碰手记节与已冻结月页；日更节奏 = 部署侧 cron 定时无人值守会话（全机械，失败源 log 报告不阻断他源）
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

<!-- plugin:structure v0.3 -->
- vault 结构声明 `wiki/structure.md`（type: structure）：frontmatter `structure` 块映射 = 目录→一句话语义，正文写预设（日期/格式/类型/混合，可嵌套）与说明；agent 放置资产先读此页按位落放；页面缺席 = 平铺容忍；人调整 vault 后同步声明，check 机械 diff（未声明的顶层目录 / 声明不存在的目录 → warning）
<!-- /plugin:structure -->

<!-- plugin:user-profile v0.2 -->
- 用户画像 `wiki/profile.md`（type: profile）：对使用者的持续认知档案，静态身份层 + 动态偏好层，维度不枚举；收敛式更新——新值取代旧值、正文留痕；断言必带证据 wikilink（会话页或 vault 代理页），偏好层挂 stale_after；零自有字段复用 trust，不属 notes 领地；个性化决策（称呼、风格、偏好）前先读此页，库未初始化时可缺
<!-- /plugin:user-profile -->

<!-- wiki-inject:end -->
