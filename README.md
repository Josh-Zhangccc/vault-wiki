# vault-wiki

**团队维护的 agent 知识库框架**：vault 容纳真实资产，wiki 做 md 代理与原生笔记，agent 按 SASU-L 披露顺序零先验读写。md 加纯文件是底座；Obsidian 等仅为可替换 viewer。

> 状态：原型已冻结——2026-09-08 到 09-12 构建，经两轮真实操作与冷启动披露审计；当前阶段为日常使用、边用边改。2026-10-02 起由个人自用转为团队项目，沿革见 `log.md`；普世化与矩阵化测试仍搁置。

## 它做什么

让 AI 编程助手替你经营一座「个人维基」：

- 资产放进 `vault/`，任意格式——md、txt、csv、pdf、图像皆可。**映射**命令登记为 `wiki/vault/` 下的 md 代理页，含 SHA-256、元数据与链接
- 对话中的洞见与决策，**保存**命令沉淀为 `wiki/notes/` 原生笔记；会话骨干页入 `wiki/sessions/`
- **检索**命令先读热缓存与索引再综合回答，产出带 wikilink 引用的答案
- 索引、标签、热缓存、运行日志全为派生层自动维护；**检查**命令审计库健康；**插件**命令装卸结构插件
- 外部源以域接入：lark 与 email 落指针或档案页；calendar 管时间线、cron 管定时任务；project 管项目容器；bb 经 bb-cli 拉取课件、作业与成绩；bilibili 经 bili-cli 现拉即答（搜索/详情/字幕/收藏夹/UP 主追踪，视频摘要与评价明示入库，低危写白名单须用户明示）。域外翻译，wiki 内全连通
- **画像**命令维护对使用者的持续认知档案：断言带证据，偏好会过期；个性化决策前先读它
- **讲解答疑**命令按认知档案个性化讲解——已知略讲或反问，未知讲透；显著答疑沉淀 ai 笔记
- **出题自测**命令按范围加样例生成英文试题与中文解析；作答后判分回流认知档案
- **认知档案**命令读写各课 user.md 学习状态；讲解与出题两条通道的用法挂载于此

## 核心概念

| 概念 | 定义 |
|---|---|
| wiki | md 世界，内外之分的内侧：各域投影加原生笔记加派生层 |
| domain | 域；wiki 外信息源的适配器契约。vault 是默认域，lark、project、email、bb、bili 亦域 |
| vault | 默认域，真实资产仓库；命令侧只增，删改自由属于人 |
| SASU-L | 披露范式：agent 只经 system prompt、AGENTS.md、Skills、用户原话、loop 获知信息 |

## 布局

| 目录 | 内容 |
|------|------|
| `.meta/` | 原型核心。三十五插件：双根概念 domain 与 wiki；域实例族 vault、lark、project、email、bili 及 cuhksz 学校域族（基座 cuhksz，域内 bb/bb-map/bb-track/bb-teach/bb-quiz、sis、registry）及域内件 mapping、structure、lark-docs、lark-im、lark-calendar；横切件 calendar、cron、notes、sessions、link、tag、trust、index、hot、log、user-profile、todo、language、device、tmp。无分层；注入序为依赖拓扑加字母序；全局件可声明桥，必依桥由内核校验域基座挂边完备。另有十三命令主本、协议工件——registry、actions、experiments——与机械脚本 wiki_plugin_kernel、pipeline、wikilib，纯标准库零依赖 |
| `connectors/` | 连接器主本：部署侧 CLI 事实接口加 skill 使用披露。`connectors/*/SKILL.md` 经 kernel deploy 落 `.agents/skills/`；现有 bb-cli、sis-cli、mail-cli、bili-cli |
| `wiki/`、`vault/`、`projects/`、`cuhksz/` | 数据区骨架。保持空种子：内容属部署实例，工程内不积累；跑库验证走 test-repo，用法见 [.meta/docs/sandbox.md](.meta/docs/sandbox.md) |
| `.agents/skills/` | 命令与连接器 skill 部署副本 |
| `test-repo/` | 独立测试沙箱。白名单式追踪：仅 `.meta/` 与 `.agents/` 框架镜像入库，随根侧同步重拷；沙箱内实验内容只在本地、不入史；内部不感知本工程 |
| `.meta/docs/` | 人的文档：`intro.md` 导论、`mechanics.md` 机制详解、`usage.md` 使用指南、`quickstart.md` 部署走查、`research-*.md` 调研档案，直达链接见文末。机制权威源在内核参考 skill，docs 不镜像机制 |

## 协作

本仓库是团队项目。三条全员红线在此摘要；权威源为 `AGENTS.md`「用户要求」节：

1. **入库边界**：仅开发产物入 git——`.meta/` 含 `docs/`、`connectors/`、根级章程、根级数据容器空种子 `cuhksz/`、test-repo 白名单镜像，镜像仅 `.meta/` 与 `.agents/`，随根侧同步重拷。永不入库：真实课程、成绩、提交数据；个人隐私；凭据会话；沙箱实验产物，即 test-repo 白名单外一切。禁止上传任何使用痕迹。
2. **git 纪律**：经分支开发，进 `master` 由管理者审合。所有者已委托 agent 代行管理：审红线、跑校验、合并推送、治理远端分支；历史改写、豁免、删人工作等保留事项仍须所有者明示。一次提交只做一件事；提交信息格式 `模块: 概述`；合并前自查 diff 不含非开发内容；禁止改写历史。
3. **提交流程**：拉分支；小步提交；自检——kernel all 通过、diff 无非开发内容、log 仅增；push 后开 PR 报审；管理者审合并通报。
4. **协作对齐**：改插件或连接器前先读 `log.md` 对表现状与下一步；版本号沿 changelog 递进、不预占跳号；实验与测试一律落沙箱或本地，结论走对话报告或 `.meta/docs/`。组员对 `log.md` 仅增不改不整；超限随分支流转并升级；整合归负责人。

## 上手

前提：Python 3，纯标准库，无需安装依赖，连接器另需各自依赖；git；能读 AGENTS.md 与 skills 的 agent 环境，如 ZCode；Obsidian 可选，仅作 viewer。

在仓库根打开 agent 会话即可。AGENTS.md 是宪法，含插件注入区；十三个命令以自然语言触发：**映射 / 保存 / 画像 / 检索 / 检查 / 插件 / 飞书映射 / 课程映射 / 资产读取 / 内核参考 / 讲解答疑 / 出题自测 / 认知档案**，对应 map、save、profile、query、check、plugin、lark-map、bb-map、asset-read、wiki_plugin_kernel、bb-teach、bb-quiz、bb-track，主本见 `.meta/command/`。把文件放进 `vault/`，对 agent 说「映射」，就是第一次使用。

## 部署

框架本体三件：`.meta/`、`.agents/skills/`、AGENTS.md 注入区。部署是 additive 拷贝：拷两棵树，写 AGENTS 外壳，建空目录，内核收敛；目标库存量内容不动。派生页首跑自建，无需手造。逐步走查见 [.meta/docs/quickstart.md](.meta/docs/quickstart.md)，经干净目录彩排验证。

## 文档指针

- `AGENTS.md` — 宪法、准则与全员硬性约束，agent 先读
- [.meta/docs/intro.md](.meta/docs/intro.md) — 导论：为什么是这样一个框架，叙事与谱系
- [.meta/docs/mechanics.md](.meta/docs/mechanics.md) — 机制详解：每机制展开一级，bb 族实例走查；动手改框架先读
- [.meta/docs/usage.md](.meta/docs/usage.md) — 使用指南：库经营、课程学习、协作开发三循环
- [.meta/docs/quickstart.md](.meta/docs/quickstart.md) — 快速开始：部署五步与首跑验证
- `log.md` — 工程日志：现状、阶段、过往操作
- `.meta/protocol/` — 字段注册表、动作纪律、披露范式

## 沿革

2026-08-26 以个人库结构副本起建；08-28 重定位为本工程；09-08 起插件加命令原型直接落地，经真实操作验证后冻结。09-12 重构：概念双插件 wiki 与 vault 立设；原 vault 插件更名 mapping；废除分层；标识符英文化。09-19 lark 族与 calendar 时间领地立设。09-22 域化：domain 双根概念立设，vault、lark、project 三实例合规。09-29 画像独立命令；email 域立设；连接器位立设。10-01 到 10-02 bb 域三件套立设并经四课实验验证；全员协作红线立规；转为团队项目。10-04 bb 认知消费侧改造——bb-teach、bb-quiz、bb-track 命令；机制文档开卷；docs 迁 `.meta/docs/`。10-05 cuhksz 学校域立设，bb 降为域内族，sis 与 registry 子域随立。10-06 bilibili 域立设（查询即答 + 涌现档案，低危写白名单），连接器 bili-cli 首版；cron 时间自动化领地立设（声明为源、每任务一页），lark-calendar/bili/email 挂桥随迁。设计谱系讨论存于个人库，见 AGENTS.md 指针。
