# 同类产品与范式调研：信息的入库与出库

> 开发侧调研档案（2026-09-16，四路并行网络检索蒸馏：官方文档 / 论文 / HN·Reddit 社区）：vault-wiki（受 llm-wiki 启发）的市场对标依据。非实例运行件。统一四问框架：**信息组合（入库）怎么做、信息检索（出库）怎么做、成功点与吸引人之处、问题与缺陷**。

## 1. 谱系源头：llm-wiki 与 OKF

### 1.1 Karpathy「LLM Wiki」gist（2026-04-04）

- **本体**：Karpathy 发布的 GitHub Gist（纯 idea file，无代码，设计为直接粘贴给任意 agent）。核心主张：RAG（含 NotebookLM、ChatGPT 上传文件）每次提问"从零重新发现知识"、无复利；替代方案是让 LLM 增量构建并维护持久 markdown wiki——"knowledge is compiled once and then kept current, not re-derived on every query"，即**写入时蒸馏 vs 查询时检索**的对立。人类放弃维护 wiki 是因为负担增长快于价值，而 LLM 不会厌倦、不会忘更新交叉引用。思想上溯 Bush 1945 Memex。
- **结构**：三层——raw sources（人工策划、不可变、LLM 只读）→ the wiki（LLM 全权生成维护）→ the schema（CLAUDE.md/AGENTS.md 约定）；三操作 Ingest/Query/Lint；两个特殊文件 index.md 与 log.md。（gist 刻意抽象；坊间"raw/wiki/output 三文件夹"说系二手演绎。）
- **成功点**：token 实测收益显著（r/ClaudeAI 案例 47,450 → 360 tokens，另有 71.5× 案例）；纯文件零依赖、Obsidian 兼容；知识复利。
- **缺陷**：初始编译与持续维护本身高耗 token（2000 个 md 文件会打爆 rate limit，r/ObsidianMD 质疑帖）；蒸馏阶段的错误与幻觉会固化进 wiki；对普通用户门槛偏高。
- **衍生实现**：nvk/llm-wiki（1.3k★，命令集 + AGENTS.md，自述 inspired by Karpathy）、nashsu/llm_wiki（19.6k★，Tauri 桌面应用 + 知识图谱）、awesome-llm-wiki 清单等。autoresearch（karpathy 官方仓库，~96k★）是 ML 训练自动化、与 wiki 无关，但社区常将"循环研究-归档"衍生模式与之合流传播。

### 1.2 Google OKF——Open Knowledge Format（2026-06-13）

- **本体（证实）**：Google Cloud 官方博客「How the Open Knowledge Format can improve data sharing」+ 规范仓库（GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md，v0.1 起步现已 v0.2）。自述定位：**把 llm-wiki 模式形式化为可移植、可互操作的开放格式**，博客原文引用 Karpathy 承认思想源头。
- **契约**："Just markdown + Just files + Just YAML frontmatter"；每概念一文件、**文件路径即身份**；唯一必填字段 `type`，约定 title/description/resource/tags/timestamp；保留文件名 index.md、log.md；markdown 链接织成关系图。三原则：minimally opinionated / producer-consumer independence / **format, not platform**（不绑定云、数据库、模型、agent 框架）。
- **入库**：参考实现 enrichment agent 遍历 BigQuery 数据集为每表草拟概念文档，二次 LLM pass 补引文/schema/join path。**出库**：静态 HTML 单文件图可视化（无后端）。
- **反响**：正面偏探索——vs RAG/GraphRAG 对比文、企业 agent 知识层讨论、开发者自建 superset、r/LLMDevs 辩论适用边界。注意与 Open Knowledge **Foundation**（CKAN，政府开放数据门户，血缘很远）撞缩写。
- **与本工程 `01-okf.md` 的趋同**（两边独立蒸馏，同出 Karpathy 谱系）：

| 契约点 | Google OKF | 本工程 01-okf.md v0.2 |
|---|---|---|
| type 必填、值集实例侧定 | ✓ | ✓（registry 封闭） |
| 保留名 index.md / log.md | ✓ | ✓（+豁免义务） |
| 一概念一文件、路径即身份 | ✓ | ✓（wikilink 全名=路径） |
| 最小 YAML、复杂结构不受理 | ✓ | ✓（顶层标量/块列表/一级块映射） |
| 生产消费解耦 | producer-consumer independence | SASU-L 零先验 |
| 信任与溯源 | **无** | **trust 四字段 + actor 统一格式 + 水位推导**（差异化强项） |

### 1.3 kepano/obsidian-skills（2026-01）

Obsidian CEO kepano 官方 agent skills 仓库，遵循 Agent Skills 开放规范（agentskills.io），现约 48.4k★。现六技能：obsidian-markdown / obsidian-bases / json-canvas / obsidian-cli / defuddle / knap（末者为后增，内部档案记的五技能少此一项）。纯文件哲学：agent 直接读写 Markdown/Bases/JSON Canvas。缺陷：obsidian-cli 1.12 社区实测 13 处静默失败（57 场景中 22.8% 退出码 0 但返回空/错数据），催生第三方补救 skill。

### 1.4 邻近参照

- **DeepWiki**（Cognition）：免费为任意公开 GitHub 仓库 AI 生成可对话文档；争议在未经维护者同意即生成 + 准确性遭质疑。
- **OKFN/CKAN**：数据集发布与发现系统，面向政府/机构开放数据，与 agent 个人知识库血缘远。

## 2. AI 原生知识库产品（C 端 PKM）

| 产品 | 入库（组合） | 出库（检索） |
|---|---|---|
| NotebookLM | notebook 为单位传 source（PDF/Docs/URL/音视频），写入近零加工 | source-grounded RAG，行内引用角标；Audio Overview 播客式摘要 |
| Notion AI | workspace 即语料 + connectors 同步 Slack/Jira/Drive | 跨页 + connector 数据 Q&A，附来源链接 |
| Mem | 快速捕获，AI 自动打标关联，零手动组织 | Smart Search 语义检索 + Related Notes 自动浮现 |
| Reflect | daily notes + 剪藏 + 语音转录；AI 自动补实体 backlinks | backlink 网络浏览 + 全文搜索 + 内置 AI 对话 |
| Tana | 会议转录/AI capture；supertag 给节点套 schema，写入时加工字段 | live searches 动态聚合视图 + Ask AI |
| Reor | 指向 md 目录，写入时本地切块+嵌入存 LanceDB | 本地语义搜索 + related notes + 本地 LLM RAG，全程离线 |
| Khoj | 同步 markdown/PDF 进索引（写入时嵌入），开源自托管 | 自然语言搜索 + 带来源问答，后端可接 Ollama |
| Obsidian 插件 | Smart Connections 全量本地嵌入持续增量 | 侧栏实时相关笔记 + 语义搜索；Copilot Vault QA 带引用 |
| MyMind | 一键保存，AI 自动打标+摘要，零组织 | smart search（关键词+语义） |

**成功点**：NotebookLM 的 grounding + 可溯源引用被视为抗幻觉标杆，Audio Overview 是破圈引爆点（第三方聚合口径称用户超 3000 万，转述数据仅供参考）；Notion 背靠存量用户零迁移成本；Mem 搜索口碑与 $23.5M 融资；Reor Show HN 411 分且获 kepano 公开背书"纯 markdown 文件优于数据库"；Khoj/Obsidian 插件吃"数据不出本地 + 复用既有 vault"卖点。

**缺陷**（各家实证）：NotebookLM 假引用/引文对不上仍存在，PDF 表格识别差、约 50 万字后严重不准，源数上限长期被抱怨；Notion 效果高度依赖 workspace 组织质量、问 database 常检索失败、付费墙变更引发不满；Mem 2.0 前长期 bug 致用户流失，自动组织的代价是分类逻辑不属于自己；Tana 学习曲线陡峭；Reor 作者自认"RAG is fairly naive"、本地 7B 模型是硬天花板；Khoj 部署门槛高且"self-hosted"宣传与 OpenAI 依赖不符；Obsidian 插件 Vault QA 需先全量嵌入、多语言 vault 语义关联差；MyMind 自动标签不准反而难找回。

**光谱小结**：一端**写入时重加工**（Mem/Reflect/MyMind 自动打标、Reor/Smart Connections 写入时嵌入），一端**近零加工、查询时再算**（NotebookLM/Notion/Tana live search）。写入时加工换检索速度但会固化错误——自动标签不准是共性翻车点；查询时加工保原文纯净但贵且慢。"带可点击引用的 RAG 问答"已成标配卖点，而"假引用"也是各家共同的信任裂缝。

## 3. Agent 记忆系统

### 3.1 产品级

- **ChatGPT Memory**：saved memories（bio 工具写成条目注入 system prompt）+ reference chat history（Embrace The Red 实测：并非检索历史对话，而是持续聚合的纵向画像——偏好推断、话题摘要、近约 40 轮用户消息原文、设备/意图元数据——整体注入，纯写时加工）。成功在零配置默认开启、可逐条删除；缺陷在画像区用户不可审计不可编辑、容量小（Plus 很快写满）、画像可被对话注入污染、GDPR 顾虑下欧洲不可用。
- **Claude（Projects / memory tool / 2026-08 统一记忆）**：产品侧 chat 与 Cowork 共享记忆、按 Project 分区、默认开启。API 侧 memory tool 是**客户端文件式记忆**：六命令操作 `/memories` 目录，Claude 自主决定记什么，系统提示强制"先看记忆目录再做事"，并按"上下文随时可能被重置"的假设持续落盘。文件即记忆、心智模型极简；缺陷是应用侧须自实现 handler 与防护、无内置去重/冲突消解。

### 3.2 框架级（star 数为 2026-09 口径）

- **Mem0（65.4k★）**：抽取-整合两阶段——`add()` 时 LLM 抽事实级记忆，决策引擎对旧记忆 ADD/UPDATE/DELETE/NOOP（OSS v3 已简化为 ADD-only，纠错须显式 update/delete）。出库四信号融合（向量+关键词+实体加分+时间意图）。官方数据 LoCoMo 92.5、token 约为全上下文 1/3–1/4。缺陷：抽取有损且非确定，细节在"事实化"时丢失；HN 批评"只做存取、不学模式"。
- **Zep / Graphiti（30.9k★）**：增量构建**时序知识图谱**，双时态——事实带 valid/invalid 时间窗，过时事实"失效而非删除"，episode 永久保留溯源。出库混合检索（嵌入+BM25+图遍历）+图距离重排，支持"当前真值/任意历史时点"查询。缺陷：每 episode 多次 LLM 调用，入库延迟与成本高。
- **Letta（前身 MemGPT，24.8k★）**：OS 式分层——上下文当 RAM、外存当磁盘，记忆为命名 blocks、agent 工具调用自编辑；sleep-time compute 空闲期后台反思改写共享记忆块。关键实验：**Letta Filesystem 仅把对话历史存文件，LoCoMo 得 74.0%，超过多数专用记忆库**。缺陷：抽象层级多、学习曲线陡，自编辑可能写坏记忆。
- **MemOS（11.4k★）**：论文以 MemCube 统三态记忆（明文/激活 KV-cache/参数 LoRA）+ Memory Scheduler 调度；开源落地为多 Cube 知识库与 traces/policies/world models 分层，三态转换多停留论文层。学术野心最大，概念重、缺第三方验证。
- **Cognee（30.7k★）**：ECL 管道（Extract-Cognify-Load）转知识图谱+嵌入，含 session distillation 与本体约束去重；`recall` 自动路由图/向量混合检索。代码知识图谱是差异化；LLM 图谱抽取是成本瓶颈，独立评测抽取质量 2.97/5。
- **LangMem / LangGraph memory**：按心理学三分 semantic/episodic/procedural，特色是 procedural 通道热更新 system prompt。概念清晰、教程生态最广；但更像 SDK，无图无时序，schema 全靠用户自设计。

### 3.3 学术侧

MemGPT（arXiv:2310.08560，范式源头）；A-MEM（arXiv:2502.12110，Zettelkasten 式原子卡片，LLM 生成链接/标签，新记忆加入触发旧记忆网络动态重组）；HippoRAG 2（ICML 2025，仿海马索引理论，离线建 KG + 查询时单次图遍历完成多跳联想）。

### 3.4 LoCoMo benchmark 争议（信任危机样本）

Mem0 论文报 Zep 65.99% → Zep 发《Lies, Damn Lies, & Statistics》指控配置错误、自报 84% → Mem0 CTO 反诉（分母剔除操纵、私改提示，10 次重跑 Zep 仅 58.44%±0.20）。**第三方元分析**：LoCoMo 约 6.4% 题目真值损坏；GPT-4o-mini 判官放行率 62.81%；**全上下文基线约 73% 反超多数专用记忆库**；同一系统在不同评测方手里得 38%–92% 不等。净结论：静态记忆榜单基本不可信，评测须自建并带全上下文/grep 基线——外部佐证本工程"以用代验、不做矩阵测试"的裁定。

## 4. Multi-agent 合作范式

**共享载体四分**：消息流（AutoGen、OpenAI Agents SDK 的 items）· 状态/检查点（LangGraph、ADK）· 向量记忆库（CrewAI）· **文件与文档**（Anthropic 附录建议、Manus、Claude Code、MetaGPT）。vault-wiki 属文件派。

**四重点**：

1. **Anthropic 多 agent 研究系统**（2025-06 博客）：orchestrator-worker，内嵌 scaling 规则（简单事实 1 个 subagent / 复杂研究 10+）；上下文隔离，subagent 各带干净上下文，lead 只收压缩结果。**官方附录明确建议：subagent 产出写入文件系统、只回传轻量引用**——避免大输出在对话历史层层复制。Opus 4 lead + Sonnet 4 workers 比单 agent 高 90.2%，token 用量可解释 80% 性能方差；代价：multi-agent 约 15× token，模糊指令致 subagent 撞车重复劳动，非确定性难调试，官方明言不适合需共享上下文的紧耦合任务。
2. **Claude Code**：记忆全文件化——分层 CLAUDE.md（企业/项目/用户级）、skills 以 SKILL.md 文件夹按需渐进披露、subagent 本身就是 md 定义。subagent 独立上下文只见任务+宪法+git 快照，仅最终摘要回流。官方警告臃肿宪法会被无视（每行须过"删掉会出错吗"测试）。
3. **Manus context engineering**：**文件系统为终极上下文**——无限大、天然持久、agent 可直接操作；todo.md 计划外置反复重写，对抗 lost-in-the-middle；上下文 append-only 稳定前缀保 KV-cache（缓存 $0.30 vs 未缓存 $3.00/MTok，10×）。承认缺陷：长上下文性能衰减、重复 trace 致模型模仿旧模式。
4. **OpenAI Agents SDK**：会话即 items 列表，Session 在 run 前 prepend/后 append，多 agent 可共享 session 互相可见；handoff 默认**广播全历史**（可用 filter 裁剪），input_type 只传小元数据。缺陷：guardrails 职责错位、长链路 token 膨胀需自建 filter。

**速写**：AutoGen 群聊即共享记忆，每条消息全员可见，官方自建议"先单 agent，确需协作再上 team"；CrewAI 整合策略最显式（相似度 >0.85 触发 LLM 仲裁 keep/update/delete、≥0.98 去重、复合评分语义 0.5/新近 0.3/重要 0.2）；LangGraph 双轨 checkpointer（会话快照）+ Store（跨线程共享 KV），checkpoint 累积推高延迟；MetaGPT（70.4k★）SOP 编码、共享记忆即结构化文档工件（用户故事→PRD→设计→代码）流转，代价是流程刚性；MCP 管工具外置（已捐 Linux Foundation，事实标准），与 wiki 管 agent 间共享记忆互补；Google A2A 走**不共享内存**路线（Agent Card 发现 + task/artifact 传递，护 IP），同厂 ADK 的 session state 为 KV 字典、长期记忆配 Memory Bank，默认 InMemory 重启即失且存原始全史"可能淹没模型"。

## 5. 横向对比

| 代表 | 记忆载体 | 入库（组合） | 出库（检索） | 信任/溯源 |
|---|---|---|---|---|
| llm-wiki（Karpathy） | md 文件 | LLM 写入时蒸馏，raw 只读 | index + 浏览 | 无（log.md 记操作） |
| Google OKF | md + YAML | enrichment agent 草拟+二次 pass | 静态图可视化 | 约定 timestamp，无信任模型 |
| **vault-wiki** | **md + YAML** | **命令纪律显式组合（map/save），raw=vault 只增** | **热缓存→索引→grep→正文渐进披露** | **trust 四字段+水位推导** |
| NotebookLM | 源文件+切块 | 写入近零加工 | 查询时 RAG + 引用角标 | 行内引用（偶有假引用） |
| Mem0 | SQL+向量+实体 | LLM 抽取+决策引擎整合 | 四信号融合 | 无时序语义 |
| Zep/Graphiti | 时序知识图谱 | 增量抽实体边+双时态 | 混合检索+图重排 | 双时态（最强时序溯源） |
| Letta | 记忆块+文件 | agent 自编辑+闲时反思 | 核心块常驻+archival 向量 | 无 |
| ChatGPT Memory | 私有画像 | 写时聚合注入 | 无独立检索层 | 不可审计（最弱） |
| Anthropic 多agent | 消息流+文件 | orchestrator 整合，建议落文件回传引用 | 上下文隔离+摘要回流 | 引用回填专职 agent |
| Manus | 文件系统 | append-only+todo.md 外置 | 全量保留+KV-cache | 可还原（URL/路径指针） |

## 6. 共性成功点与共性缺陷

**成功点**：① 复利效应——"编译一次持续保鲜"取代"每次重推"（llm-wiki、Mem0 选择性更新、Zep 失效不删除）；② 有据可查的引用成为信任卖点（NotebookLM 角标、Notion 链接）；③ 纯文件 + 路径即身份（OKF format-not-platform、kepano 背书、Letta Filesystem 实验、Claude memory tool 同向）；④ 渐进披露控制 token（index→正文、skills、Audio Overview）；⑤ 零配置默认开启降低大众门槛（ChatGPT Memory）。

**缺陷**：① 抽取有损且非确定（Mem0/Zep/Cognee 通病，不可复现）；② 蒸馏错误固化——wiki 里的幻觉没有自然纠错回路（llm-wiki 最大软肋，check/lint 是生命线）；③ 假引用与审计缺口（NotebookLM 引文对不上、ChatGPT 画像不可编辑）；④ token 成本（multi-agent 15×、wiki 维护费、全量嵌入费）；⑤ benchmark 军备竞赛与真实使用脱节（LoCoMo 争议，全上下文基线反超）；⑥ 自动组织的失控感与"让思考变被动"的哲学质疑（Mem/MyMind）。

## 7. 对 vault-wiki 的启示

**已获外部验证的选型**：md 纯文件底座（OKF 三原则、kepano 论证、Letta Filesystem 74.0%、Claude memory tool 文件记忆——四路独立佐证）；路径即身份 ↔ wikilink 全名约定；index.md/log.md 保留名已成谱系惯例；hot 热缓存 ≈ Manus todo.md 反漂移 + 渐进披露；trust 四字段恰好补上 Google OKF 与 NotebookLM 都缺的信任层；"以用代验"裁定与 LoCoMo 信任危机互证。

**可借鉴**：Anthropic"产出写文件系统、回传轻量引用"可明写进 save/map 的 usage；Zep"失效而非删除"与 trust 的 stale_after/verified 事件列表同构，可强化"过时知识不删只标记"的语义；Letta sleep-time compute 对应本工程"闲时整合 log"（须用户同意的既有边界不变）；CrewAI 的整合阈值证明 save 去重可量化，但数值机械化须防过拟合。

**风险警示**：蒸馏错误固化——check 必须保持硬约束地位；wiki 维护的 token 成本随页数膨胀——hot ≤25 条与索引聚合度是现有闸门，需持续观察；**OKF 命名撞车**（Google Open Knowledge Format / Open Knowledge Foundation）——`01-okf.md` 全称未定待所有者补记，是否与 Google OKF 对齐或显式区分是决策点。

## 8. 来源（分组择要）

- **谱系**：Karpathy LLM Wiki gist（gist.github.com/karpathy/442a6bf555914893e9891c11519de94f）· Google OKF 博客（cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing）· OKF 规范（github.com/GoogleCloudPlatform/knowledge-catalog，okf/SPEC.md）· kepano/obsidian-skills（github.com/kepano/obsidian-skills）· nvk/llm-wiki（github.com/nvk/llm-wiki）· nashsu/llm_wiki（github.com/nashsu/llm_wiki）· token 案例（r/ClaudeAI 1sfdztg）· hype 质疑（r/ObsidianMD 1sx040s）· CLI 静默失败（forum.obsidian.md/t/111169）
- **知识库产品**：NotebookLM（blog.google Audio Overviews；r/notebooklm 1l2aosy）· Notion AI（workflowautomation.net 评测；r/Notion 1g7gx3h）· Mem（techcrunch 2022-11-10 融资）· Reflect（reflect.app/blog）· Tana（producthunt.com/products/tana）· Reor（news.ycombinator.com/item?id=39372159）· Khoj（github.com/khoj-ai/khoj）· Smart Connections（community.obsidian.md）
- **agent 记忆**：Mem0（docs.mem0.ai/core-concepts/how-it-works；arxiv 2504.19413）· Zep/Graphiti（github.com/getzep/graphiti）· Letta（letta.com/blog/sleep-time-compute；letta.com/research）· MemOS（arxiv 2505.22101；github.com/MemTensor/MemOS）· Cognee（github.com/topoteretes/cognee）· LangMem（langchain-ai.github.io/langmem）· ChatGPT Memory 拆解（embracethered.com 2025 chatgpt-how-does-chat-history-memory-preferences-work）· Claude memory tool（platform.claude.com/docs）· 争议（blog.getzep.com/lies-damn-lies-statistics；github.com/getzep/zep-papers/issues/5；essays.bloo-mind.ai/posts/2026-05-20-mem-eval）
- **multi-agent**：Anthropic 多 agent 系统（anthropic.com/engineering/built-multi-agent-research-system）· Claude Code（code.claude.com/docs/en/best-practices；/sub-agents）· Manus（manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus）· Agents SDK（openai.github.io/openai-agents-python）· AutoGen（microsoft.github.io/autogen）· CrewAI（docs.crewai.com/concepts/memory）· LangGraph（docs.langchain.com langgraph/persistence）· MetaGPT（github.com/FoundationAgents/MetaGPT；arxiv 2308.00352）· MCP（modelcontextprotocol.io）· A2A（a2a-protocol.org）· ADK（cloud.google.com/blog remember-this-agent-state-and-memory-with-adk）
