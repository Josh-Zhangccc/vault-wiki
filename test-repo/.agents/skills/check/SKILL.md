---
name: check
owner: framework
description: "审计库的健康状态：底座与插件硬结构检查 + 插件与页面语义检查。Triggers on: check, 健康检查, 检查插件, lint."
---

# check：库健康审计

审，不防。输出分级报告：error = 结构破损需处理；warning = 提示待办。检查规则来自两处：本文件底座部分（协议级）+ 下方注入区（wiki_plugin_kernel 自各插件 manifest checks 列表机械化投影，在场即注册）。

## Purpose

对整个实例（底座 + 插件 + wiki 页面）做一次健康审计。

## Scope

读：全部（.meta/、AGENTS.md 注入区、.agents/skills/、wiki/、vault/ 目录树）
写：wiki/log.md 一行（type "check"）；可再生区按动作纪律直接重建（脚本：注入区 / registry / 命令副本；语义：索引 / tags / hot 淘汰 / log 归档 / 哈希重算）

## Steps

1. **底座硬检查**（协议级）：
   - **静态自检脚本**：`python .meta/scripts/wiki_plugin_kernel.py validate`（目录完整、manifest 七字段 + 可选 commands、id 一致、依赖存在、无环、命令绑定 owner×commands 双向一致）——错误即 FAIL
   - **幂等重建**：`python .meta/scripts/wiki_plugin_kernel.py all`（注入区 / registry 插件段 / 命令副本——机械自动，漂移在此修复，脚本源码即规则清单）
   - `.meta/protocol/registry.yaml` 在位且 protocol / reserved 段完好（脚本不触碰这两段，缺段即报错）
   - **值集越界**：扫 wiki/ 全部页面 frontmatter，type / status 取值不在注册表值集 → error
   - `.meta/command/` 每个 SKILL.md 有 frontmatter（name / description / owner；可选 consumes——消费写侧契约的插件有序列表，引用插件须在场且带 usage 列表，owner 驱动命令必填）
2. **插件检查**：先跑附检 `python .meta/scripts/wiki_plugin_kernel.py audit`（机械项：各插件 scripts/check.py 发现式执行，只读报告，error 计入 FAIL）；再执行下方注入区块中标注「语义」的项
3. **语义检查**：读插件与命令文件，查悬挂引用（命令涉及不存在的结构）、幽灵字段（页面字段无拥有插件且非注册表预留）、注入区块与 PLUGIN.md Checks 节不一致
4. 汇总输出：PASS / WARN / FAIL 计数 + 分级明细 + vault 积压计数（信息项）
5. **修复按动作纪律分级执行**（`.meta/protocol/actions.md`）：机械自动项直接做——`pipeline.py index` / `tags`（索引重建）、`wiki_plugin_kernel.py all`（注册表 / 注入区 / 副本）、哈希重算（改 frontmatter 的 raw_sha256），hot / log 越界由各自写管道命令收敛；机械确认项呈清单问一次，语义项只报告；历史条目永不自动改
6. wiki/log.md 置顶追加一行（type "check"，走 `pipeline.py log check "<一句话>"`）；有变更（修复 / log 行）即按提交纪律入库（`检查: <结论>`，见 `.meta/protocol/actions.md`）

## Tools

grep / 读文件即够；一次读取够用的不做第二次扫描（调用节俭）。

## Parameters

- 无：全库审计
- 插件 id：只查该插件

## Injected Section (plugin check blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest checks 列表投影（`inject` / `all` 重建，在场即注册）；手写内容不进此区，改检查规则改 PLUGIN.yaml。

<!-- check-inject:start -->
<!-- check:hot -->
- 窗口越界（超 25 条 / 超 5 日 / 单条超 200 字）→ 走一次 `pipeline.py hot <类型> "<补录>"` 或等下次写入自然收敛后复查
- 与 log 矛盾（log 有记录而 hot 全无踪迹）→ warning
<!-- /check:hot -->

<!-- check:link -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：断链（目标既非页面全名，也非任何页的 aliases）→ warning；hot 手写断链 → warning（不作入链源）；乱码链接（目标含 U+FFFD 替换符，含 related 项）→ error；别名二义（两页声明同一 aliases，解析不确定）→ error；孤儿页（无入链且无 related 引用，入链源只计概念页）→ notes 知识页 warning、领地值登记页 info（registry 领地值除 session，暂无入链为登记常态）；related 单向（A 列 B 而 B 未回列）→ 信息
- 语义项（check 命令）：入链密度 top 榜 → 信息项（hub 涌现依据，不告警）
<!-- /check:link -->

<!-- check:log -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：无日期条目（`- ` 开头而不匹配日期格式，主文件与归档同检）→ error
- 语义项（check 命令）：历史条目被修改（git 可核）→ error；容量超限 → 机械归档后复查
<!-- /check:log -->

<!-- check:notes -->
- 笔记被命令覆盖的痕迹 → error
- 近似重复笔记（Jaccard > 0.7）→ warning
<!-- /check:notes -->

<!-- check:sessions -->
- 机械项（audit 覆盖）：session 型页面在 `wiki/sessions/` 之外（或反向）→ warning；participants 缺失或项不符 actor 约定 → warning
- 语义：骨干页过度膨胀（该提升未提升）→ warning
<!-- /check:sessions -->

<!-- check:tag -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：单页 >5 个 tag → warning；tags 复述 type → warning；层级超限（父/子 ≤2）或空段 → warning
- 语义项（check 命令）：近重复 tag → warning 提示合并；合并为机械确认项（呈清单，用户确认后执行）
<!-- /check:tag -->

<!-- check:trust -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：generated 缺 by/at 或 actor 格式错、verified 事件缺 by/at 或格式错、stale_after 非 YYYY-MM-DD、sources 非列表 → warning
- 机械项（信息级）：stale 页清单（已过 stale_after）；信任水位（human-reviewed / machine-confirmed 计数）
- 语义（check 命令）：stale 页处置分诊（刷新时刻 / 重验证 / 废弃）——人决
<!-- /check:trust -->

<!-- check:calendar -->
- 语义项（v0.1 人工，附检后置）：月页文件名非 YYYY-MM 或落 wiki/calendar/ 之外 → error；已过月份月页改写痕迹 → error（git 审计）；声明页缺 `calendar` 块 → info（manual-only 常态）
<!-- /check:calendar -->

<!-- check:index -->
- 索引与实际页面集偏差（含该删未删的并回索引）→ 跑 `pipeline.py index` 重建即修复（幂等，无 diff 即一致）；tags 同理（`pipeline.py tags`）
- 手编痕迹 → warning
<!-- /check:index -->

<!-- check:lark -->
- 语义项（v0.1 人工，附检后置）：指针页缺 token / token 重复 → error；lark.profile 与所在目录名不符 → warning；type: lark 落 wiki/lark/ 之外 → error；域枢纽页（docs.md 等）落 profile 目录之外 → warning
<!-- /check:lark -->

<!-- check:mapping -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：镜像 diff（vault 有文件无代理 → info 积压；代理无对应物 → error，报文含引用计数——删前见影响面）、缺登记字段（raw_file / raw_sha256）→ error、raw_file 悬挂 → error、raw_sha256 失配 → warning、疑似全文复制（md 资产正文 ≥80% 原文）→ warning、无描述 stub 且 updated 超 90 天 → warning
- 语义项（check 命令）：失配处置分诊（描述仍适用 → 机械重算自动修复，毕即写 log 行（类型 map，一句话含资产名与「原文已变，描述仍适用」）；疑似失效 → 人决重映射或删）；日记类全文复制豁免判断；孤儿代理处置前先处置引用（同步改引用或留 aliases 重定向）
<!-- /check:mapping -->

<!-- check:structure -->
- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：声明 diff——vault 顶层目录未声明 → warning、声明键指向不存在目录 → warning；type: structure 落 `wiki/structure.md` 之外 → error；声明页缺席 → info（平铺容忍）
<!-- /check:structure -->

<!-- check:todo -->
- 机械项（信息级）：日期触发已逾期且未销账条目清单（开 session 提醒的机械依据）；页面缺失（未受托常态）
- 机械项：条目缺触发条件或 by/at → warning；type: todo 落 `wiki/todo.md` 之外 → error
- 语义（check 命令）：open 条目 > 50 → warning（膨胀分诊：该做的做、该沉淀的走 save、该放弃的与用户确认）
<!-- /check:todo -->

<!-- check:lark-calendar -->
- 语义项（v0.1 人工）：声明页 lark 源的 profile 不在 wiki/lark/ 目录集 → warning；日程行源键无对应声明 → warning
<!-- /check:lark-calendar -->

<!-- check:lark-docs -->
- 语义项（v0.1 人工，附检后置）：`docs.md` 缺 `docs` 块映射 → warning；指针页落 `docs/` 子树之外 → warning；kind 不在词表 → info
<!-- /check:lark-docs -->

<!-- check:lark-im -->
- 语义项（v0.1 人工，附检后置）：群档 / 人档缺 token → error；kind 落 chat|person 之外 → error；type: lark 页落 im/ 之外而自称本域 → warning；人档沉淀区空白 → info（骨架常态）；正文沉淀区改写痕迹 → error（git 审计）
<!-- /check:lark-im -->

<!-- check:user-profile -->
- 语义（check 命令）：画像断言缺证据 wikilink → warning
- 机械项：type: profile 页面落 `wiki/notes/` 或 `wiki/vault/`（走错领地）→ error
- 机械项（信息级）：画像页缺失（库未初始化属正常，初始化机制定案后再定升降级）
<!-- /check:user-profile -->
<!-- check-inject:end -->
