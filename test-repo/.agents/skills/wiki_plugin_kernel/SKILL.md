---
name: wiki_plugin_kernel
owner: framework
description: "内核与机制参考：投影机七子命令（ls/validate/audit/inject/registry/deploy/all）+ 插件机制全述——manifest / 依赖 / 三投影 / 命令绑定 / 桥法则 / 分层原则（bb 域贯穿示例）。Triggers on: 插件内核, wiki_plugin_kernel, kernel, 注入块更新, 投影重建, 插件机制, 更新注入."
---

# wiki_plugin_kernel：内核与机制参考

`python .meta/scripts/wiki_plugin_kernel.py <子命令>`——框架侧唯一投影机：PLUGIN.yaml 是本体，AGENTS 注入区、check 检查块、命令用法块、注册表插件段、命令与连接器 skill 副本全是它的投影。幂等，随时可跑，漂移即修复。本 skill 兼作**机制总纲**：部署实例只带 AGENTS.md 注入区 + skills 副本即自足，本文件是机制原理在部署侧的权威住所。

## 子命令

| 子命令 | 作用 | 写盘 |
|---|---|---|
| `ls` | 插件清单 + 依赖 + 驱动命令 | 无 |
| `validate` | 合规检查：manifest 字段、依赖无环、owner×commands 双向一致、consumes 在场且带 usage 列表、桥法则；错误退出码 1 | 无 |
| `audit` | 附检：发现式执行各插件 `scripts/check.py`，只读报告（可带插件 id 只查一个） | 无 |
| `inject` | 重建三种投影：AGENTS 注入区 + check 检查块 + 命令用法块 | AGENTS.md、含注入区的命令 SKILL.md |
| `registry` | 重建 registry.yaml 插件段（自各 manifest `fields`） | registry.yaml |
| `deploy` | 同步 skill 主本（`.meta/command/*/` 命令 + `connectors/*/` 连接器）→ `.agents/skills/` 副本；孤儿副本仅报告（删除属人） | 副本 |
| `all` | validate + inject + registry + deploy 一步到位 | 以上全部 |

## 典型场景

- **改了 PLUGIN.yaml**（inject / checks / usage / fields / 版本）：`python .meta/scripts/wiki_plugin_kernel.py all`——日常标准动作，一条命令全部收敛；validate 不过则阻断，修完重跑
- **只刷注入块**：`inject` 够用，但注意它改的是 `.meta/command/` 主本，副本须 `deploy` 才同步——所以日常一律用 `all`
- **健康快检**：`validate`（结构）+ `audit`（附检）；完整审计（含语义项）走 check 命令
- **装卸插件**：语义流程（决策、目录归档、log 行）走 plugin 命令；其中的机械步骤即本 CLI 的 `validate` / `all` / `audit`
- **改了连接器 skill**（`connectors/*/SKILL.md` 主本）：跑 `deploy`（或 `all`）同步副本——连接器 skill 不进 `.meta/command/`（命令族纯 wiki 操作）

## 插件形态

- **一插件一目录**（`.meta/plugins/<id>/`）：`PLUGIN.yaml`（manifest，机器可读本体）+ `PLUGIN.md`（纯文档：Role / Structure / Invariants / Changelog——**设计理由与各件细节归此**，机制共性归本参考）+ 可选 `scripts/check.py`（附检）
- **manifest 键**：必填七键 `id / version / depends / updated / attachment / fields / inject`；可选 `commands`（本插件驱动的命令名）、`usage`（写侧契约列表——第三投影源）、`checks`（检查规则列表——check 投影源）、`bridge`（桥声明，见桥法则）
- **attachment** = 声明领地与借读关系（谁拥有哪片路径、谁只读消费谁的页）；**fields** = 自有页面字段（进 registry，全局词表）；**inject** = 注入区一行（宪法级披露，agent 进库即知）
- **附检契约**：`scripts/check.py` 定义 `check(ctx)` 返回 `[{level, message}]`；只读零副作用，修复归命令/人；AST 静态校验契约形状

## 依赖机制

- `depends` 声明行为或语义依赖（如桥接件依赖两端概念插件）；validate 校验存在性与无环（DFS）
- **域件** = depends 链可达 `domain`；直接 depends domain 者为**域基座**（vault / lark / project / email / bb）。域内件经传递属域，不必直连 domain
- **注入序 = 依赖拓扑（被依赖者先注入）+ 同批字母序**——消费侧插件在生产者披露在场之后注入（如 bb-track 先于 bb-teach / bb-quiz），无分层概念
- 域须在 wiki 内可发现（声明页或注入行）；域件不立根容器——课程/域内产物住域领地（双侧 `<term>/<course>/` 同构），泛用容器（vault）或指针为默认姿态

## 命令-插件绑定

- **owner × commands 双向声明**：命令 SKILL.md frontmatter `owner: 插件id`（或 `framework`，显式无主），插件 manifest `commands: [命令名]`；任一侧单边声明即 error
- **consumes（跨插件投影）**：命令 frontmatter `consumes: [有序插件列表]`——序即执行序；owner 驱动的命令必填且含全部 owner；各被消费插件的 `usage` 列表自动投影进该命令 SKILL.md 的 `cmd-inject` 标记块
- 首例：bb-track 命令 `consumes: [bb-track, bb-teach, bb-quiz, trust, log]`——认知枢纽聚合采集通道用法，装卸自动增删（在场即注册）
- **披露在消费现场**原则：集成格式的权威源是 usage（随投影到达命令），不是插件散文——见桥法则末条

## 投影机制（三投影一源）

- **manifest 是唯一文本源**，kernel 向三处机械投影，全部幂等重建、装卸自动同步：
  1. **AGENTS.md 注入区**（`wiki-inject:start/end` 标记块）← `inject` 行——宪法级，每插件一块
  2. **check 检查块**（check 命令内 `check-inject:start/end`）← `checks` 列表——语义项检查规则
  3. **命令用法块**（各命令内 `cmd-inject:start/end`）← `usage` 列表按 consumes 序——写侧契约
- 第四处机械投影：**registry.yaml 插件段** ← `fields`（字段全局词表）；第五处：**skill 副本**（deploy）
- 手写区与机械区严格分界：标记块内禁手编（重建即覆写），块外正文属人；改契约 = 改 manifest → `all` 收敛，**不存在第二事实源**

## 桥法则（宪法准则 11）

- **全局件**（横切服务与归宿：trust / log / todo / calendar / notes / user-profile…）可声明**桥**——manifest `bridge: 必依|按需`；**域件**不得持桥（depends 链可达 domain 者，持桥即 error）
- **必依桥**：全部域基座必须有对应 depends 边，缺边即 error（拓扑完备性不变量——如 log 必依桥保证任何域的产生必有痕迹）；**按需桥**：缺席容忍（消费侧跳过不报错，如 user-profile 认知桥）
- **桥与 cmd-inject 的分工**（2026-10-04 裁定）：桥持**校验与声明**（谁可挂、基数、完备性检查、缺席容忍）；披露分发归投影（集成格式细则的权威源 = usage，随 cmd-inject 到达消费现场，零检索成本）——桥节（PLUGIN.md）退为详述，不持格式权威。桥不可被 cmd-inject 替代的内核：必依完备校验是拓扑约束，consumes 表达不了；且领地间写入（todo/calendar/notes 派生）发生在一切命令执行中，无单点命令容器可挂载

## 分层原则（域内示例：bb 四件族）

- **素材层在 bb/（外工作区），档案层在 wiki/（内属地）**：过程产物（拉取物、人的笔记、ai 笔记、考卷判分）住素材层；沉淀的结论（认知读数、投影页）住档案层——「bb/ notes/ 人为主 ai 共居」与「user.md 域内原生页」即此分层的实例
- 一个域的生长路径：**domain 契约六问**（外领地 / 落地策略 / 身份证明 / wiki 属地 / 写模型 / 信任模型）→ 域基座立领地（如 bb v0.7：双侧同构 + notes/ 共居）→ 域内件族（bb-map 投影法则、bb-track 认知档案）→ 消费侧采集通道（bb-teach / bb-quiz：零领地工作流件，用法经 consumes 挂枢纽命令）——**消费侧插件可以是最薄的形态**（零自有字段，只贡献 usage 与检查规则）
- 数据流闭环示例：teach 讲解 → ai 笔记落 notes/（弱证据）→ track 消费收敛 → quiz 出题参照 → 判分回流证据流（machine 证据）——素材产生、档案提炼、采集回写三段各归其件

## 边界

- 脚本只碰四处：插件目录进出、注入区标记块、registry 插件段、skill 部署副本；protocol / reserved 段与 AGENTS.md 手写区永不动
- 纯标准库零依赖（Python 3）；中文输出
- 数据区派生层（`wiki/index.md`、`tags.md`、`hot.md`、`log.md`）不归本 CLI——那是 `pipeline.py`（`index` / `tags` / `hot` / `log` / `verify`），由 map / save 的写后管道调用

## Parameters

- 子命令（见上表）；`audit` 可带插件 id
