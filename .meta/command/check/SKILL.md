---
name: check
owner: framework
description: "审计库的健康状态：底座与插件硬结构检查 + 插件与页面语义检查。Triggers on: check, 健康检查, 检查插件, lint."
---

# check：库健康审计

审，不防。输出分级报告：error = 结构破损需处理；warning = 提示待办。检查规则来自两处：本文件底座部分（协议级）+ 下方注入区（各插件经 PLUGIN.md「检查」节注入的块）。

## 用途

对整个实例（底座 + 插件 + wiki 页面）做一次健康审计。

## 涉及结构

读：全部（.meta/、AGENTS.md 注入区、.agents/skills/、wiki/、vault/ 目录树）
写：wiki/log.md 一行（类型「检查」）；可再生区按动作纪律直接重建（脚本：注入区 / registry / 命令副本；语义：索引 / tags / hot 淘汰 / log 归档 / 哈希重算）

## 步骤

1. **底座硬检查**（协议级）：
   - **静态自检脚本**：`python .meta/scripts/plugin_cli.py validate`（目录完整、manifest 八字段 + 可选 commands、id 一致、依赖方向、无环、命令绑定 owner×commands 双向一致）——错误即 FAIL
   - **幂等重建**：`python .meta/scripts/plugin_cli.py all`（注入区 / registry 插件段 / 命令副本——机械自动，漂移在此修复，脚本源码即规则清单）
   - `.meta/protocol/registry.yaml` 在位且 protocol / reserved 段完好（脚本不触碰这两段，缺段即报错）
   - **值集越界**：扫 wiki/ 全部页面 frontmatter，type / status 取值不在注册表值集 → error
   - `.meta/command/` 每个 SKILL.md 有 frontmatter（name / description / owner）
2. **插件检查**：先跑附检 `python .meta/scripts/plugin_cli.py audit`（机械项：各插件 scripts/check.py 发现式执行，只读报告，error 计入 FAIL）；再执行下方注入区块中标注「语义」的项
3. **语义检查**：读插件与命令文件，查悬挂引用（命令涉及不存在的结构）、幽灵字段（页面字段无拥有插件且非注册表预留）、注入区块与 PLUGIN.md 检查节不一致
4. 汇总输出：PASS / WARN / FAIL 计数 + 分级明细 + VAULT 积压计数（信息项）
5. **修复按动作纪律分级执行**（`.meta/protocol/actions.md`）：机械自动项直接做——`pipeline.py index` / `tags`（索引重建）、`plugin_cli.py all`（注册表 / 注入区 / 副本）、哈希重算（改 frontmatter 的 raw_sha256），hot / log 越界由各自写管道命令收敛；机械确认项呈清单问一次，语义项只报告；历史条目永不自动改
6. wiki/log.md 置顶追加一行（类型「检查」，走 `pipeline.py log 检查 "<一句话>"`）

## 工具

grep / 读文件即够；一次读取够用的不做第二次扫描（调用节俭）。

## 参数

- 无：全库审计
- 插件 id：只查该插件

## 注入区（各插件检查块）

<!-- check:vault -->
- 机械项（audit 覆盖）：镜像 diff（积压 = 信息 / 孤儿 = error）、raw_file 悬挂 = error、raw_sha256 失配 = warning、疑似全文复制 = warning、stub 超 90 天 = warning
- 语义：失配处置分诊（描述仍适用 → 机械重算自动修复；疑似失效 → 人决重摄入或删）；日记类全文复制豁免
<!-- /check:vault -->

<!-- check:log -->
- 历史条目被修改（git 可核）→ error；无日期条目 → error；容量超限 → 机械归档后复查
<!-- /check:log -->

<!-- check:hot -->
- 窗口越界（超 25 条 / 超 5 日 / 单条超 200 字）→ 机械淘汰或截短后复查；与 log 矛盾 → warning
<!-- /check:hot -->

<!-- check:tag -->
- 机械项（audit 覆盖）：单页 >5 → warning；复述 type → warning
- 语义：近重复 tag → warning 提示合并（合并 = 机械确认项：呈清单，确认后批量改 frontmatter）
<!-- /check:tag -->

<!-- check:notes -->
- 笔记被命令覆盖痕迹 → error；近似重复（Jaccard > 0.7）→ warning
<!-- /check:notes -->

<!-- check:sessions -->
- 机械项（audit 覆盖）：session 型页在 wiki/sessions/ 之外（或反向）→ warning；participants 缺失或项不符 actor 约定 → warning
- 语义：骨干页过度膨胀（该提升未提升）→ warning
<!-- /check:sessions -->

<!-- check:link -->
- 断链（目标既非页面全名，也非任何页 aliases）→ warning（尚未写下的知识，TODO 占位属正常）；乱码/畸形链接 → error
- 孤儿页（无入链且无 related 引用；入链源只计概念页——index/hot/log/tags 与 archive/ 等派生页不算源）→ warning；入链密度 top 榜 → 信息项（hub 涌现依据）
<!-- /check:link -->

<!-- check:index -->
- 索引与实际页面集偏差 → `pipeline.py index` 重建（自动，不询问）；tags 同理（`pipeline.py tags`）；手编痕迹 → warning
<!-- /check:index -->
