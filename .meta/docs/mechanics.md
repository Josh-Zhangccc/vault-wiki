# 机制详解

> 读者：要动手改框架的组员与贡献者。机制规则的权威源是内核参考 skill 与 `.meta/` 源码。本文把总纲展开一级：原理、实例走查与动手流程，不复制规则原文；与源冲突时以源为准。撰写 2026-10-04。

## 0. 一源五投影

每个插件一个目录，住 `.meta/plugins/<id>/`。`PLUGIN.yaml` 是机器可读本体，即 manifest。内核脚本从 manifest 出发，向五处机械投影：

| 投影 | 落点 | 源键 | 谁在读 |
|---|---|---|---|
| AGENTS 注入区 | `<!-- plugin:<id> v<x> -->` 标记块 | `inject` | 每个 session 的 agent；宪法级披露 |
| check 检查块 | check 命令内 `check-inject` 块 | `checks` | 检查命令；语义项规则 |
| 命令用法块 | 各命令内 `cmd-inject` 块 | `usage`，按 consumes 序 | 命令执行现场；写侧规则 |
| registry 插件段 | `.meta/protocol/registry.yaml` | `fields` | 写页前查字段词表的命令 |
| skill 副本 | `.agents/skills/<命令>/` | 命令与连接器主本 | 部署侧 agent |

关键性质是幂等重建。标记块内禁手编，重建即覆写；块外正文属人。不存在第二事实源：改规则就是改 manifest，随后 `all` 一条命令收敛。文档漂移这一类问题被整类消灭——投影与本体不会不一致，因为它们不是两份东西。

走查一粒真实样本。bb-quiz 的 manifest 里 `inject:` 是一行中文，说明出题自测做什么、产物落在哪。`all` 跑完，这行字逐字出现在 AGENTS 注入区 `<!-- plugin:bb-quiz v0.2 -->` 块里。agent 日常读到的是投影；装卸插件时才碰 manifest 本体。

## 1. 插件形态

一插件一目录，三件套：

- `PLUGIN.yaml` — manifest，本体
- `PLUGIN.md` — 纯文档：设计概要、Structure、Invariants、Changelog。为什么这样设计归此；机制共性归内核参考
- `scripts/check.py` — 可选附检。定义 `check(ctx)` 返回 `[{level, message}]`，只读零副作用；形状由 AST 静态校验

manifest 七个必填键，以 bb-quiz v0.2 的真实值示意：

| 键 | 语义 | 实例 |
|---|---|---|
| `id` / `version` / `updated` | 身份与版本；沿 changelog 递进不跳号 | `bb-quiz` / `0.2` / `2026-10-04` |
| `depends` | 依赖列表 | `[bb-track, bb-map]` |
| `attachment` | 领地声明：拥有即写，借读即只读消费 | 见下 |
| `fields` | 自有页面字段；进 registry 全局词表 | `quiz`，考卷块映射 |
| `inject` | 注入区一行的源；宪法级披露 | 见 AGENTS bb-quiz 块 |

可选键四个。`commands` 声明本插件驱动的命令；`usage` 是写侧规则列表；`checks` 是检查规则；`bridge` 是桥声明，仅全局件可持。

attachment 值得单独看。bb-quiz 声明了三条：

- `bb/<term>/<course>/notes/testing/` 是考卷子区，本插件拥有。每测一组试题加答案；判分追记在答案页
- `wiki/bb/<term>/<course>/user.md` 是认知档案，归 bb-track。本插件只读；判分回写要经 bb-track 的写规则
- `courseware/` 与 `assessments/` 归 bb-map。本插件只读，取 sm-N 锚点、专有名词表和已知作业

第一条是拥有，后两条是借读：领地属别的插件，写路径要经其规则。attachment 就是框架的产权登记。谁拥有哪片路径、谁只读消费谁，一眼可查，机械可检。

## 2. 依赖与注入序

`depends` 声明依赖。validate 校验两件事：依赖存在，且无环——环路由 DFS 检出。

域件是 depends 链可达 `domain` 的插件。直连 domain 者为域基座，即 vault、lark、project、email、bb 五件；域内件经传递属域，不必直连。bb-quiz 不直连 domain：它经 `bb-quiz → bb-track → bb-map → bb → domain` 到达，即为域件。

注入序 = 依赖拓扑加同批字母序：被依赖者先注入，同批按名字排。看 bb 族的 depends 与注入区真实顺序：

| 插件 | depends | 效果 |
|---|---|---|
| bb | `[domain, wiki, trust, log]` | 域基座，族内最先注入 |
| bb-map | `[bb, wiki]` | 映射法则，在 bb 之后 |
| bb-track | `[bb, bb-map, trust, wiki]` | 认知档案，在 bb-map 之后 |
| bb-quiz / bb-teach | `[bb-track, bb-map]` | 采集通道；同批按名字，quiz 先于 teach |

这保证一件事：消费侧插件注入时，它消费的披露一定已在场。bb-teach 的注入行说「纪律见 bb-track 块」，那块必然在它上面。另有一条域纪律：域须在 wiki 内可发现，声明页或注入行皆可；域件不立根容器。

## 3. 投影走查

假设要给 bb-quiz 的写侧规则加一条纪律，会发生什么：

1. 改 `.meta/plugins/bb-quiz/PLUGIN.yaml` 的 `usage:` 列表，加一行。顺手 `version` 进位、`updated` 刷新；PLUGIN.md 的 Changelog 加一行
2. 跑 `python .meta/scripts/wiki_plugin_kernel.py all`。依次发生：validate 先行，不过则阻断，修完重跑；若 inject 行也改了，AGENTS 注入区重建；bb-quiz 与 bb-track 两个命令 SKILL 主本的 cmd-inject 块重建——usage 出现在所有 consumes 含 bb-quiz 的命令里；registry 插件段重建；skills 副本同步
3. 自查 diff。变更只应落在 manifest、两个命令 SKILL 主本、`.agents/skills/` 副本；若动了 inject 或 fields，AGENTS 与 registry 也变。此外任何变更都是异常
4. 提交，格式 `插件: bb-quiz …`；一次提交只做一件事

这是「一源五投影」的日常体感：你只写了一份东西，五处自动一致。

## 4. 命令绑定

owner 与 commands 双向声明。命令 SKILL.md frontmatter 写 `owner: 插件id`，或写 `framework` 表示显式无主；插件 manifest 写 `commands: [命令名]`。任一侧单边声明即 validate error——防命令没人管，也防插件虚报命令。

用法落向命令有两条路。**拉取侧**：命令 frontmatter 写 `consumes: [插件列表]`，声明要拉取哪些插件的用法；owner 驱动的命令必填且含全部 owner。**源侧路由**：插件 manifest 写 `usage_routes: [命令名列表]`，声明自己的用法额外落向哪些命令——装插件即落投影，无需改目的地命令。在场即注册在推侧兑现：装卸单文件生效。validate 校验路由目标在场、路由件带 usage、与 consumes 重复即 error。

披露序是呈现序：owner 块在前，按 consumes 序；路由块居中，按依赖拓扑加字母序；其余 consumes 殿后。

首例走查，看 bb-track 命令这个认知枢纽。bb-track 命令只声明 `consumes: [bb-track, trust, log]`；bb-teach 与 bb-quiz 各在 manifest 声明 `usage_routes: [bb-track]`。`all` 之后，bb-track 命令的 SKILL.md 里出现五个 `<!-- usage:<id> -->` 子块：bb-track 自己的写规则、bb-quiz 与 bb-teach 两条采集通道的完整用法、trust 与 log 的写侧规则。效果：任何 agent 走进 bb-track 命令现场，教与考怎么用、判分怎么回流、写后做什么，一次到位，零检索。将来立第三条采集通道，只需新插件写好 usage 加路由声明，投影自动到场，枢纽命令一字不改。

用法路由全程可查走 `ls`：每个带 usage 的插件列出落向哪些命令；无落向的标注为契约文档面，如 email 声明先立的写侧契约。

## 5. 桥法则

全局件是横切服务与归宿：trust、log、todo、calendar、notes、user-profile。它们可声明桥；域件持桥即 error。

必依桥在 manifest 写 `bridge: 必依`：全部域基座必须有对本件的 depends 边，缺边即 validate error。log 是实例——第 2 节表里 bb 的 depends 中那条 `log` 边就是必依桥所迫：任何域的产生必有痕迹。这是拓扑完备性不变量，不是风格建议。

按需桥在 manifest 写 `bridge: 按需`：缺席容忍。user-profile 的认知桥是实例——bb-track 建档时画像在场才登记一行；缺席跳过不代建，不报错。

为什么 consumes 替代不了桥，2026-10-04 裁定给出两条硬理由：

1. 必依完备校验是拓扑约束。「五个域基座一个都不能少挂边」是图上的全局不变量；consumes 是单命令的列表，表达不了全局完备性
2. 领地间写入发生在一切命令执行中。todo 派生、calendar 派生、notes 涌现不经过某个单点命令容器，没有可以挂 consumes 的地方

分工：桥持校验与声明——谁可挂、基数、完备性检查、缺席容忍；披露分发归投影——集成格式的权威源是 usage，随 cmd-inject 到达消费现场。

## 6. 派生层

内核管框架区，即插件与投影；pipeline 管数据区，即 wiki 派生页。命令是 `python .meta/scripts/pipeline.py index / tags / hot / log / verify`：

- **index / tags**：目录索引与标签反向索引。纯函数重建，只聚合不发明结构；某索引清单超窗时切子目录自立索引——解药是分子目录，不是改索引
- **hot**：最近变更热缓存。至多 25 条、5 日内、单条 200 字以内；agent 进库先读
- **log**：运行日志写行与滚动归档。窗口至多 100 条，超限机械归档到 `wiki/archive/月/log.md`
- **verify**：写后一致性检查。map、save 等命令的写后管道以它收尾

派生页与投影是同一哲学的两种应用：投影从 manifest 派生，框架侧无第二源；派生页从库内容派生，数据侧无第二源。手编派生页是徒劳的，下次重建即覆写。

## 7. 装卸生命周期

装卸的语义流程走 plugin 命令，agent 做语义部分；机械步骤即本 CLI。

装，五步：准备 `.meta/plugins/<id>/` 三件；`validate`，错误阻断；`all`，投影到场；冒烟——`audit <id>`，加按 PLUGIN.md 关键流程走一遍；log 记 plugin 行。

升，三步：改插件，`version` 进位，Changelog 加行；`all`；log 行。

卸，四步：`validate`，有插件依赖它即阻断，除非用户显式级联；目录移出——归档留存，物理删除永远属人；`all`，投影随之消失；log 行。

纪律：脚本错误一律阻断，警告仅报告；版本沿 changelog 递进，不预占跳号。

## 8. 域的生长

框架对 wiki 外的信息源不设白名单。接入是回答同一份契约，生长遵循同一条路径。以 bb 族贯穿，它是最完整的一族。

### 契约六问

设计一个域就是逐问作答。答案落进域基座的领地声明与注入行：

| 问 | bb 族的答案 |
|---|---|
| 外领地在哪 | bb.cuhk.edu.cn，连接器 bb-cli 纯只读 |
| 落地策略 | 双侧同构：`bb/` 工作区加 `wiki/bb/` 属地 |
| 身份证明 | 学期名与课程代码目录，加 bb 块映射 machine id |
| wiki 侧属地 | `wiki/bb/<term>/<course>/`，bb-map 四桶投影 |
| 写模型 | 拉取物只增；notes/ 人为主，ai 产物只增不覆写 |
| 信任模型 | machine-confirmed 天花板；stale_after = 拉取日 + TTL |

### 写模型三分

落地本质是写模型选择，三个原型：

- **终态资产 → 只增仓储**。真身落地后不再变，如 vault 资产、bb 物化课件。命令侧只增，删改自由属于人
- **过程容器 → 全权读写**。agent 要在其中工作，如 `projects/`、bb notes/ 的 ai 产物
- **真相在别处 → 指针**。源头会变，本地不需要副本，如 lark 指针页、bb 媒体类默认指针化。stale_after 管时效；agent 即同步器

### 投影密度

投影密度随翻译成本递减，三档。**镜像**：1:1 代理，如 mapping。**指针**：token 加 url 加快照选段，如 lark。**仅披露**：一行注入加按需现拉，如 email 检索。默认姿态是借 vault 或指针；自立容器是例外——何时例外：写模型分叉，或结构由源硬性规定。bb 因双侧结构刚性自立。

### 生长路径

契约之后：**域基座**立领地，bb 是双侧同构加 notes/ 共居；**域内件族**跟进——bb-map 投影法则、bb-track 认知档案，形态渐重；**消费侧采集通道**收尾——bb-teach 与 bb-quiz 零领地纯工作流，用法经源侧路由挂枢纽命令。族内依赖链 `bb-quiz → bb-track → bb-map → bb` 即此路径的机械表达，见第 2 节。

### 素材与档案

域内两分。过程产物住域工作区：拉取物、人的笔记、ai 笔记、考卷判分。沉淀结论住 wiki 属地：投影页、认知读数。wiki 收蒸馏物，不收过程。这条线与全局纪律同构，只是落到了域内。

### 连接器

连接器住 `connectors/`，是域的部署侧 CLI 事实接口加使用披露：`connectors/<名>/SKILL.md` 经 kernel `deploy` 落 `.agents/skills/` 副本。与命令的区别：命令是纯 wiki 操作，主本在 `.meta/command/`；连接器是对外部系统的取数通道，凭据只存本机、不入库、不落盘。域插件声明领地与纪律，连接器提供事实接口。纪律与工具分离。

## 9. 场景速查

| 你想做 | 动作 |
|---|---|
| 改写侧规则 / 检查规则 / 注入行 | 改 manifest 对应键，跑 `all` |
| 给命令挂新插件的用法 | 该插件 manifest 写 `usage`；命令 frontmatter consumes 加 id；跑 `all` |
| 改连接器 skill | 改 `connectors/*/SKILL.md` 主本，跑 `deploy` 或 `all` |
| 健康快检 | `validate` 加 `audit`；完整审计走 check 命令 |
| 装卸插件 | plugin 命令做语义，本 CLI 做机械 |
| 重建数据区派生页 | `pipeline.py index` 或 `tags`；hot 与 log 随写随维护 |
| 接一个新外部源 | 答契约六问，见第 8 节；写连接器；plugin 命令装域基座与域内件 |
