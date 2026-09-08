# 项目介绍

本仓库（目录 `agent-obsidian-template`，工程暂名 **vault-wiki**）不是任何 vault 的副本，而是「普世 vault-wiki 框架」的构建工程：产出让任何人（任何 agent）建立「把任意格式信息存储为资产的 vault」所需的骨架、准则、技能与工具。

- 产出物：`skeleton/`（通用骨架：目录结构 + 实例宪法模板 + 通用准则）、`skills/`（薄壳技能）、`scripts/`（lint 与格式解析器）、`docs/`（设计文档）
- 核心定义：vault = 把任意格式的信息存储为资产的容器；wiki = 信息 → md 解析的管道；个性化是动态内容，不属于架构
- 设计上游是 `docs/00-principles.md`：下游产出与其冲突时，先改上游再改下游
- 个人库（`D:\Obsidian repo\agent-obsidian`）是本框架的第一个回填实例，不是设计输入

# 核心准则

1. **设计先行**：每条准则先在 `docs/` 立稿、讨论、定稿，再落地为 skeleton / skills / scripts；draft 状态的设计不落地。
2. **骨架与实例分离**：个人化的东西（日记体系、素材偏好、称呼规则……）一律记为实例配置项，不进架构。试金石：搬不进一个全新实例的，就是个人层漏进了架构。
3. **架构不枚举**：不枚举文件格式（只设格式 → 解析器注册表）、不枚举笔记类型（类型是 frontmatter 字段，目录只反映流水线工位）。
4. **无工具私有格式**：md + 纯文件是底座；Obsidian、WebUI 等都是可替换 viewer。
5. 主动维护 `log.md`：含项目现状、阶段与进度、下一步计划、过往操作；总量不超过 2k 字；操作标注日期（精确到天）；描述过时或过长时主动整合压缩，**整合须先征得用户同意**。
6. 本文件为指导性文件，总长度 <150 行；详细信息用指针引用；每个 session 开始时主动读取重要指针。
7. 产出文档以中文为主，结构文件用 ASCII 文件名。
8. **小步主动提交**：设计定稿或骨架变更落地后，agent 主动 git commit，不等用户指令（防零提交陷阱）；提交信息格式 `模块: 概述`（如 `骨架: 定稿最小集与目录结构`），一次提交只做一件事；不主动 push；禁止改写历史的操作。

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
- `docs/00-principles.md` — 普世定义与设计原则（上游，冲突时以它为准）**ATTENTION**
- `skeleton/` — 通用骨架（产出）；`skills/` — 薄壳技能（产出）；`scripts/` — 工具（产出）
- `README.md` — 项目章程（产出物清单与工作方式）
- 设计谱系（讨论记录，只读）：个人库 `wiki/meta/2026-08-25-wiki运行时重构决策.md`、`wiki/sessions/2026-08-25-wiki架构调研与docs-first重构设计.md`
- 参考工程：`D:\My Programs\erp - ksbgs`（AGENTS.md 模式来源：宪法+指针、log 容量管理、指令集）；`D:\My Programs\aijia`（wiki 指针化引用）

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:tag v0.1 -->
- 页面 `tags` 字段：YAML 列表，中文为主、英文专名小写 kebab-case，层级 `父/子` ≤2，每页 ≤5；开放语义分类，禁止复述 type
<!-- /plugin:tag -->

<!-- plugin:vault v0.1 -->
- 代理层 `wiki/vault/`：与根 `vault/` 1:1 镜像（代理名 = 原名 + .md），页面必有 raw_file / raw_sha256；路径即出身证明；命令对 VAULT 只增，删改自由属于人
<!-- /plugin:vault -->

<!-- plugin:log v0.1 -->
- 运行日志 `wiki/log.md`：置顶追加、只增不删，条目 = 日期 + 类型（摄入/保存/检查/装卸/其他）+ 一句话；每次写操作后记一行
<!-- /plugin:log -->

<!-- plugin:hot v0.1 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条且 <5 日），agent 进库先读此页
<!-- /plugin:hot -->

<!-- plugin:notes v0.1 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识（概念/问答/决策/会话），细分靠 type 字段；不可再生区，命令只增不改
<!-- /plugin:notes -->

<!-- plugin:index v0.1 -->
- 索引 `wiki/index.md`（全库清单）/ `wiki/tags.md`（tag 反向索引）：只聚合、永不手编，检索第二入口
<!-- /plugin:index -->

<!-- wiki-inject:end -->
