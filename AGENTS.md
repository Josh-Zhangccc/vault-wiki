# 项目介绍

本仓库（目录 `agent-obsidian-template`，工程暂名 **vault-wiki**）是 vault-wiki 框架的构建工程，兼第一个**原型实例**：2026-09-08 起「插件 + 命令」架构直接落地，规范文档后置蒸馏。

- 布局：`.meta/`（插件与命令主本，原型核心）· `wiki/` + `vault/`（数据区）· `.agents/skills/`（部署副本）· `user-write/`（用户手稿，agent 只读）· `docs/`（设计档案）；`skeleton/`、`skills/`、`scripts/` 为旧计划遗留空目录
- 术语：**VAULT** = 真实资产仓库（命令侧只增，删改自由属于人）；**wiki** = VAULT 的 md 代理层与原生笔记；**vault**（小写）= 拥有代理层的结构插件
- 冲突裁决：以原型现状与讨论收敛结论为准；规范蒸馏时归并 `docs/` 历史版本
- 个人库（`D:\Obsidian repo\agent-obsidian`）为只读实证样本：原 wiki 思想已转化为本原型（见 log 2026-09-08）

# 核心准则

1. **原型先行、doc 后置**：设计经讨论收敛后直接落地为原型（`.meta/` 插件与命令），以真实操作验证；规范文档事后从跑通的现实蒸馏，不预先立稿。
2. **骨架与实例分离**：个人化的东西（日记体系、素材偏好、称呼规则……）一律记为实例配置项，不进架构。试金石：搬不进一个全新实例的，就是个人层漏进了架构。
3. **架构不枚举**：不枚举文件格式与笔记类型（类型是 frontmatter 字段）；结构由插件各自规范，wiki 目录只分代理层（`wiki/vault/`）与原生笔记区（`wiki/notes/`）。
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
- `.meta/` — 原型核心：结构插件（`plugins/`）与命令主本（`command/`）与协议工件（`protocol/`：字段注册表、动作纪律）与机械脚本（`scripts/`：装卸/合规/注入/副本）；AGENTS.md 注入区为其投影 **ATTENTION**
- `user-write/` — 用户手稿（概述、设计初衷、插件规范草案），agent 只读
- `wiki/`、`vault/` — 数据区（当前为种子状态）；`.agents/skills/` — 命令部署副本
- `docs/00-principles.md` — 历史设计档案（已精简，规范蒸馏时归并）
- `README.md` — 项目章程（待随现状更新）
- 设计谱系（讨论记录，只读）：个人库 `wiki/meta/2026-08-25-wiki运行时重构决策.md`、`wiki/sessions/2026-08-25-wiki架构调研与docs-first重构设计.md`
- 参考工程：`D:\My Programs\erp - ksbgs`（AGENTS.md 模式来源：宪法+指针、log 容量管理、指令集）；`D:\My Programs\aijia`（wiki 指针化引用）

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

<!-- plugin:notes v0.4 -->
- 原生笔记 `wiki/notes/`：出身在 wiki 的知识（概念/问答/决策/会话），细分靠 type 字段；不可再生区，命令只增不改
<!-- /plugin:notes -->

<!-- plugin:vault v0.5 -->
- 代理层 `wiki/vault/`：与根 `vault/` 1:1 镜像（代理名 = 原名 + .md），页面必有 raw_file / raw_sha256；路径即出身证明；命令对 VAULT 只增，删改自由属于人
<!-- /plugin:vault -->

<!-- plugin:link v0.3 -->
- 链接语法 `[[页面全名]]`（禁截断式引用，同名歧义带路径）；字段 `related` / `aliases`；断链 = warning（尚未写下），孤儿（无入链无引用，派生页不算源）= warning
<!-- /plugin:link -->

<!-- plugin:tag v0.3 -->
- 页面 `tags` 字段：YAML 列表，中文为主、英文专名小写 kebab-case，层级 `父/子` ≤2，每页 ≤5；开放语义分类，禁止复述 type
<!-- /plugin:tag -->

<!-- plugin:hot v0.3 -->
- 热缓存 `wiki/hot.md`：最近变更摘要（≤25 条、<5 日、单条 ≤200 字），agent 进库先读此页；写前先淘汰越界
<!-- /plugin:hot -->

<!-- plugin:index v0.3 -->
- 索引 `wiki/index.md`（根，含 okf_version）与各目录 `index.md`（渐进披露，逐层下钻）/ `wiki/tags.md`（tag 反向索引）：只聚合、永不手编，重建走 `pipeline.py index`，检索第二入口
<!-- /plugin:index -->

<!-- plugin:log v0.4 -->
- 运行日志 `wiki/log.md`：置顶追加、条目不改写，条目 = 日期 + 类型（摄入/保存/检索/检查/装卸/其他）+ 一句话；窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`
<!-- /plugin:log -->

<!-- wiki-inject:end -->
