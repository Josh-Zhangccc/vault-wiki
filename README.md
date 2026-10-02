# vault-wiki

**团队维护的 agent 知识库框架**：vault 容纳真实资产，wiki 做 md 代理与原生笔记，agent 按 SASU-L 披露顺序零先验读写。md + 纯文件是底座，Obsidian 等仅为可替换 viewer。

> 状态：原型已冻结（2026-09-08~12 构建，两轮真实操作 + 冷启动披露审计通过），当前阶段为日常使用、边用边改。2026-10-02 起由个人自用转为团队项目（沿革见 `log.md`）；普世化与矩阵化测试仍搁置。

## 它做什么

让 AI 编程助手（agent）替你经营一座「个人维基」：

- 资产放进 `vault/`（任意格式：md / txt / csv / pdf / 图像……），**映射（map）**命令登记为 `wiki/vault/` 下的 md 代理页（SHA-256 + 元数据 + 链接）
- 对话中的洞见与决策，**保存**命令沉淀为 `wiki/notes/` 原生笔记；会话骨干页入 `wiki/sessions/`
- **检索**命令先读热缓存与索引再综合回答，产出带 wikilink 引用的答案
- 索引 / 标签 / 热缓存 / 运行日志全为派生层自动维护；**检查**命令审计库健康，**插件**命令装卸结构插件
- 外部源以域接入：lark（飞书）与 email（个人邮箱）落指针 / 档案页，calendar 管时间线，project 管项目容器，bb（Blackboard 课程域）经 bb-cli 拉取课件、作业与成绩——域外翻译、wiki 内全连通
- **画像（profile）**命令维护对使用者的持续认知档案（断言带证据、偏好会过期），个性化决策前先读它

## 核心概念

| 概念 | 定义 |
|---|---|
| wiki | md 世界，内外之分的内侧（各域投影 + 原生笔记 + 派生层） |
| domain | 域，wiki 外信息源的适配器契约（vault 是默认域，lark / project / email / bb 亦域） |
| vault | 默认域——真实资产仓库；命令侧只增，删改自由属于人 |
| SASU-L | 披露范式：agent 只经 system prompt → AGENTS.md → Skills → 用户原话 → loop 获知信息 |

## 布局

| 目录 | 内容 |
|------|------|
| `.meta/` | 原型核心：二十五插件（双根概念 domain / wiki + 域实例族 vault / lark / project / email / bb 及域内件 mapping / structure / lark-docs / lark-im / lark-calendar / bb-map，横切件 calendar / notes / sessions / link / tag / trust / index / hot / log / user-profile / todo / tmp；无分层，注入序=依赖拓扑+字母序）、九命令主本、协议工件（registry / actions / experiments）、机械脚本（wiki_plugin_kernel / pipeline / wikilib，纯标准库零依赖） |
| `connectors/` | 连接器主本：部署侧 CLI 事实接口 + skill 使用披露（`connectors/*/SKILL.md` 经 kernel deploy 落 `.agents/skills/`；bb-cli 首件） |
| `wiki/`、`vault/`、`projects/`、`bb/` | 数据区骨架（保持空种子：内容属部署实例，工程内不积累——跑库验证走 test-repo） |
| `.agents/skills/` | 命令与连接器 skill 部署副本 |
| `test-repo/` | **独立测试沙箱**：框架镜像随根侧同步重拷，沙箱内实验内容只在本地、不入史；内部不感知本工程 |
| `docs/` | 设计档案：现行 `quickstart.md` 部署走查、`pointers.md` 指针机制、`research-user-profile.md` 设计依据；历史档案 `00-principles.md`、`01-okf.md` 不起现行作用 |

## 协作

本仓库是团队项目，三条全员红线在此摘要，**权威源为 `AGENTS.md`「用户要求（硬性约束）」**：

1. **入库边界**：仅开发产物入 git——`.meta/`、`connectors/`、`docs/`、根级章程、test-repo 内框架镜像与虚构示例。**永不入库**：真实课程 / 成绩 / 提交数据、个人隐私、凭据会话、沙箱实验产物（`test-repo/bb/`、`test-repo/wiki/bb/` 等真实数据区）。`test-repo/` 是独立测试沙箱，实验内容只在本地；**发生真实实验后其内一切变更不得提交**——派生页与临时区已脱离跟踪，禁止上传任何使用痕迹。
2. **git 纪律**：经分支开发，进 `master` 须负责人确认；一次提交只做一件事，提交信息格式 `模块: 概述`；合并前自查 diff 不含非开发内容；为被忽略数据开 gitignore 白名单须仓库所有者明示授权并留痕；禁止改写历史。
3. **协作对齐**：改插件 / 连接器前先读 `log.md` 对表现状与下一步，版本号沿 changelog 递进、不预占跳号；实验与测试一律落沙箱或本地，结论走对话报告或 `docs/`。

## 上手

前提：Python 3（纯标准库，无需安装依赖；连接器另需各自依赖）、git、能读 AGENTS.md 与 skills 的 agent 环境（如 ZCode）；Obsidian 可选，仅作 viewer。

在仓库根打开 agent 会话即可——AGENTS.md 是宪法（含插件注入区），九个命令以自然语言触发：**映射 / 保存 / 画像 / 检索 / 检查 / 插件 / 飞书映射 / 课程映射 / 内核参考**（map / save / profile / query / check / plugin / lark-map / bb-map / wiki_plugin_kernel，主本见 `.meta/command/`）。把文件放进 `vault/`，对 agent 说「映射」，就是第一次使用。

## 部署：装进你自己的库

框架本体三件：`.meta/`、`.agents/skills/`、AGENTS.md 注入区。部署是 additive 拷贝——拷两棵树 + 写 AGENTS 外壳 + 建空目录 + 内核收敛，目标库存量内容不动；派生页首跑自建，无需手造。逐步走查见 [docs/quickstart.md](docs/quickstart.md)（经干净目录彩排验证）。

## 文档指针

- `AGENTS.md` — 宪法、准则与全员硬性约束（agent 先读）
- `docs/quickstart.md` — 快速开始：部署五步与首跑验证（走查）
- `log.md` — 工程日志：现状、阶段、过往操作
- `.meta/protocol/` — 字段注册表、动作纪律、披露范式

## 沿革

2026-08-26 以个人库结构副本起建，08-28 重定位为本工程，09-08 起「插件 + 命令」原型直接落地、经真实操作验证后冻结；09-12 重构：概念双插件 wiki/vault 立设、原 vault 插件更名 mapping、废除分层、标识符英文化；09-19 lark 族与 calendar 时间领地立设；09-22 域化：domain 双根概念立设，vault / lark / project 三实例合规；09-29 画像独立命令（profile）、email 域立设、连接器位立设（bb-cli）；10-01~02 bb 域三件套（基石 / bb-map 映射法则 / bb-map 命令）立设并经四课实验验证，全员协作红线立规，由个人自用转为团队项目。设计谱系讨论存于个人库（见 AGENTS.md 指针）。
