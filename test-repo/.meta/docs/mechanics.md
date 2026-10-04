# 机制详解：从 manifest 到运行时

> 读者：要动手改框架的组员与贡献者。机制契约的权威源是内核参考 skill（`wiki_plugin_kernel`）与 `.meta/` 源码；本文把总纲展开一级——原理、实例走查与动手流程。不复制契约原文，与源冲突时以源为准。撰写 2026-10-04。

## 0. 全景：一源五投影

每个插件是一个目录（`.meta/plugins/<id>/`），其 `PLUGIN.yaml`（manifest）是机器可读本体。内核脚本从 manifest 出发，向五处机械投影：

| 投影 | 落点 | 源键 | 谁在读 |
|---|---|---|---|
| AGENTS 注入区 | `<!-- plugin:<id> v<x> -->` 标记块 | `inject` | 每个 session 的 agent（宪法级披露） |
| check 检查块 | check 命令内 `check-inject` 块 | `checks` | 检查命令（语义项规则） |
| 命令用法块 | 各命令内 `cmd-inject` 块 | `usage`（按 consumes 序） | 命令执行现场（写侧契约） |
| registry 插件段 | `.meta/protocol/registry.yaml` | `fields` | 写页前查字段词表的命令 |
| skill 副本 | `.agents/skills/<命令>/` | 命令与连接器主本 | 部署侧 agent |

关键性质：全部**幂等重建**——标记块内禁手编（重建即覆写），块外正文属人；**不存在第二事实源**，改契约 = 改 manifest → `all` 一条命令收敛。这一条消灭了「文档漂移」整类问题：投影永远不会和本体不一致，因为它们不是两份东西。

走查一粒真实样本：bb-quiz 的 manifest 里 `inject:` 是一行中文（「出题自测 bb-quiz（bb-track 的 testing 消费侧）……」），`all` 之后它逐字出现在 AGENTS 注入区的 `<!-- plugin:bb-quiz v0.2 -->` 块里。agent 日常读到的是投影——装卸时（plugin 命令）才碰 manifest 本体。

## 1. 插件形态：一目录三件

- `PLUGIN.yaml` — manifest，本体
- `PLUGIN.md` — 纯文档（Role / Structure / Invariants / Changelog）：**为什么这样设计**归此，机制共性归内核参考
- `scripts/check.py`（可选）— 附检：定义 `check(ctx)` 返回 `[{level, message}]`，只读零副作用，AST 静态校验契约形状

manifest 七个必填键，以 bb-quiz（v0.2）的真实值示意：

| 键 | 语义 | 实例 |
|---|---|---|
| `id` / `version` / `updated` | 身份与版本（沿 changelog 递进不跳号） | `bb-quiz` / `0.2` / `2026-10-04` |
| `depends` | 行为或语义依赖列表 | `[bb-track, bb-map]` |
| `attachment` | 领地声明：拥有（写）与借读（只读消费） | 见下 |
| `fields` | 自有页面字段（进 registry 全局词表） | `quiz`（考卷块映射） |
| `inject` | 注入区一行的源——宪法级披露 | 见 AGENTS bb-quiz 块 |

可选键：`commands`（本插件驱动的命令）、`usage`（写侧契约列表）、`checks`（检查规则）、`bridge`（桥声明，仅全局件可持）。

**attachment 值得单独看**——bb-quiz 声明了三条：

- `bb/<term>/<course>/notes/testing/` —— 考卷子区（**拥有**：每测一组试题 + 答案，判分追记于答案页）
- `wiki/bb/<term>/<course>/user.md` —— 认知档案（**bb-track 属，只读消费**；判分回写经 bb-track 契约）
- `courseware/`、`assessments/` —— **bb-map 属，只读**（sm-N 锚点、专有名词表、已知作业）

第一条是拥有（领地），后两条是借读（领地属别的插件，写路径要经其契约）。attachment 就是框架的产权登记：谁拥有哪片路径、谁只读消费谁，一眼可查、机械可检。

## 2. 依赖与注入序

- `depends` 声明依赖，validate 校验存在性与无环（DFS）
- **域件** = depends 链可达 `domain` 的插件；直连 domain 者为**域基座**（vault / lark / project / email / bb），域内件经传递属域、不必直连。bb-quiz 不直连 domain——经 `bb-quiz → bb-track → bb-map → bb → domain` 链到达，即为域件
- **注入序 = 依赖拓扑（被依赖者先注入）+ 同批字母序**。看 bb 族的 depends 与注入区真实顺序：

| 插件 | depends | 效果 |
|---|---|---|
| bb | `[domain, wiki, trust, log]` | 域基座，族内最先注入 |
| bb-map | `[bb, wiki]` | 映射法则，在 bb 之后 |
| bb-track | `[bb, bb-map, trust, wiki]` | 认知档案，在 bb-map 之后 |
| bb-quiz / bb-teach | `[bb-track, bb-map]` | 采集通道，同批字母序（quiz 先于 teach） |

保证一件事：**消费侧插件注入时，它消费的披露一定已在场**——bb-teach 的注入行说「纪律见 bb-track 块」，那块必然在它上面。另有一条域纪律：域须在 wiki 内可发现（声明页或注入行），域件不立根容器。

## 3. 投影走查：改一条 usage 会发生什么

假设要给 bb-quiz 的写侧契约加一条纪律：

1. 改 `.meta/plugins/bb-quiz/PLUGIN.yaml` 的 `usage:` 列表（加一行）；顺手 `version` 进位、`updated` 刷新，PLUGIN.md 的 Changelog 加一行
2. `python .meta/scripts/wiki_plugin_kernel.py all`——依次发生：validate（不过则阻断，修完重跑）→ AGENTS 注入区重建（若 inject 行也改了）→ **bb-quiz 命令与 bb-track 命令**两个 SKILL 主本的 cmd-inject 块重建（usage 出现在所有 consumes 含 bb-quiz 的命令里）→ registry 插件段 → skills 副本同步
3. 自查 diff：变更只应落在 manifest、两个命令 SKILL 主本、`.agents/skills/` 副本、（若动了 inject/fields 的）AGENTS 与 registry——此外任何变更都是异常
4. 提交（`插件: bb-quiz …`）——一次提交只做一件事

这就是「一源五投影」的日常体感：**你只写了一份东西，五处自动一致**。

## 4. 命令-插件绑定与 cmd-inject

- **owner × commands 双向声明**：命令 SKILL.md frontmatter 写 `owner: 插件id`（或 `framework`，显式无主），插件 manifest 写 `commands: [命令名]`；任一侧单边声明即 validate error——防「命令没人管」与「插件虚报命令」
- **consumes（跨插件投影）**：命令 frontmatter `consumes: [有序插件列表]`，序即执行序；owner 驱动的命令必填且含全部 owner。各被消费插件的 `usage` 列表按此序投影进该命令的 `cmd-inject` 标记块

首例走查——bb-track 命令（认知枢纽）：

```yaml
consumes: [bb-track, bb-teach, bb-quiz, trust, log]
```

`all` 之后，bb-track 命令的 SKILL.md 里出现五个 `<!-- usage:<id> -->` 子块：自己的写契约（建档 / 证据 / 收敛纪律）在最前，随后 bb-teach 与 bb-quiz 两条采集通道的完整用法，最后 trust 与 log 的写侧纪律。效果：**任何 agent 走进 bb-track 命令现场，教与考怎么用、判分怎么回流、写后做什么，一次到位、零检索**。装卸自动增删——将来立第三条采集通道，只需其 manifest 写好 usage 并进 consumes，投影自动到场（在场即注册）。

## 5. 桥法则：校验归桥、披露归投影

全局件（横切服务与归宿：trust / log / todo / calendar / notes / user-profile）可声明桥；域件持桥即 error。

- **必依桥**（`bridge: 必依`）：全部域基座必须有对本件的 depends 边，缺边即 validate error。log 是实例——§2 表里 bb 的 depends 中那条 `log` 边就是必依桥所迫：**任何域的产生必有痕迹**。这是拓扑完备性不变量，不是风格建议
- **按需桥**（`bridge: 按需`）：缺席容忍。user-profile 的认知桥是实例——bb-track 建档时画像在场才登记一行，缺席跳过不代建、不报错

**为什么 consumes 替代不了桥**（2026-10-04 裁定，两条硬理由）：

1. 必依完备校验是**拓扑约束**——「五个域基座一个都不能少挂边」是图上的全局不变量；consumes 是单命令的列表，表达不了全局完备性
2. 领地间写入发生在**一切命令执行中**——todo 派生、calendar 派生、notes 涌现不经过某个单点命令容器，没有可以挂 consumes 的地方

分工：桥持**校验与声明**（谁可挂、基数、完备性检查、缺席容忍）；披露分发归投影——集成格式的权威源 = usage，随 cmd-inject 到达消费现场。

## 6. 派生层 pipeline：数据区的另一半机械

内核管框架区（插件与投影），pipeline 管数据区（wiki 派生页）：`python .meta/scripts/pipeline.py index / tags / hot / log / verify`——

- **index / tags**：目录索引与标签反向索引，纯函数重建、只聚合不发明结构；某索引清单超窗时切子目录自立索引（溢出减负制，解药是分子目录不是改索引）
- **hot**：最近变更热缓存（≤25 条、<5 日、单条 ≤200 字），agent 进库先读
- **log**：运行日志写行与滚动归档（窗口 ≤100 条，超限机械归档至 `wiki/archive/月/log.md`）
- **verify**：写后一致性检查——map / save 等命令的「写后管道」以它收尾

派生页与投影是同一哲学的两种应用：投影从 manifest 派生（框架侧无第二源），派生页从库内容派生（数据侧无第二源）——**手编派生页是徒劳的，下次重建即覆写**。

## 7. 装卸生命周期

装卸的语义流程走 plugin 命令（agent 做语义部分），机械步骤即本 CLI：

- **装**（五步）：准备 `.meta/plugins/<id>/` 三件 → `validate`（错误阻断）→ `all`（投影到场）→ 冒烟（`audit <id>` + 按 PLUGIN.md 关键流程走一遍）→ log「plugin」行
- **升**（三步）：改插件 + `version` 进位 + Changelog 行 → `all` → log 行
- **卸**（四步）：`validate`（有插件依赖它即阻断，除非用户显式级联）→ 目录移出（归档留存，物理删除永远属人）→ `all`（投影随之消失）→ log 行

纪律：脚本错误一律阻断、警告仅报告；版本沿 changelog 递进不预占跳号。

## 8. 场景速查

| 你想做 | 动作 |
|---|---|
| 改写侧契约 / 检查规则 / 注入行 | 改 manifest 对应键 → `all` |
| 给命令挂新插件的用法 | 该插件 manifest 写 `usage` + 命令 frontmatter consumes 加 id → `all` |
| 改连接器 skill | 改 `connectors/*/SKILL.md` 主本 → `deploy`（或 `all`） |
| 健康快检 | `validate` + `audit`；完整审计（含语义项）走 check 命令 |
| 装卸插件 | plugin 命令（语义）+ 本 CLI（机械） |
| 重建数据区派生页 | `pipeline.py index` / `tags`（hot / log 随写随维护） |
