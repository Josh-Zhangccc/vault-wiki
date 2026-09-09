---
name: check
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
   - **静态自检脚本**：`python .meta/scripts/plugin_cli.py validate`（目录完整、manifest 七字段、id 一致、依赖存在、无环）——错误即 FAIL
   - **幂等重建**：`python .meta/scripts/plugin_cli.py all`（注入区 / registry 插件段 / 命令副本——机械自动，漂移在此修复，脚本源码即规则清单）
   - `.meta/protocol/registry.yaml` 在位且 protocol / reserved 段完好（脚本不触碰这两段，缺段即报错）
   - **值集越界**：扫 wiki/ 全部页面 frontmatter，type / status 取值不在注册表值集 → error
   - `.meta/command/` 每个 SKILL.md 有 frontmatter（name / description）
2. **插件检查**：逐插件执行下方注入区的检查块
3. **语义检查**：读插件与命令文件，查悬挂引用（命令涉及不存在的结构）、幽灵字段（页面字段无拥有插件且非注册表预留）、注入区块与 PLUGIN.md 检查节不一致
4. 汇总输出：PASS / WARN / FAIL 计数 + 分级明细 + VAULT 积压计数（信息项）
5. **修复按动作纪律分级执行**（`.meta/protocol/actions.md`）：机械自动项直接做（重建索引 / 淘汰 hot / 归档 log / 重算哈希 / 重写注册表），机械确认项呈清单问一次，语义项只报告；历史条目永不自动改
6. wiki/log.md 置顶追加一行（类型「检查」，超 100 条先归档分流）

## 工具

grep / 读文件即够；一次读取够用的不做第二次扫描（调用节俭）。

## 参数

- 无：全库审计
- 插件 id：只查该插件

## 注入区（各插件检查块）

<!-- check:vault -->
- 镜像 diff：vault/ 有文件无代理 → 信息项（积压计数与清单）；代理无 VAULT 对应物 → error
- raw_sha256 失配 → 描述仍适用则机械重算自动修复；描述疑似失效 → warning（人决重摄入或删）
- 代理复制原文全文 → error（日记类以登记为主可豁免）；无一行描述且 updated 超 90 天 → warning（新 stub 免告）
<!-- /check:vault -->

<!-- check:log -->
- 历史条目被修改（git 可核）→ error；无日期条目 → error；容量超限 → 机械归档后复查
<!-- /check:log -->

<!-- check:hot -->
- 窗口越界（超 25 条 / 超 5 日 / 单条超 200 字）→ 机械淘汰或截短后复查；与 log 矛盾 → warning
<!-- /check:hot -->

<!-- check:tag -->
- 近重复 tag → warning 提示合并（合并 = 机械确认项：呈清单，确认后批量改 frontmatter）；单页 >5 → warning；复述 type → warning
<!-- /check:tag -->

<!-- check:notes -->
- 笔记被命令覆盖痕迹 → error；近似重复（Jaccard > 0.7）→ warning
<!-- /check:notes -->

<!-- check:link -->
- 断链（目标既非页面全名也非任何页 aliases）→ error；乱码链接（非 UTF-8 目标）→ error
- 孤儿页（无入链且无 related 引用，结构页除外）→ warning；入链密度 top 榜 → 信息项（hub 涌现依据）
<!-- /check:link -->

<!-- check:index -->
- 索引与实际页面集偏差 → 机械重建（自动，不询问）；手编痕迹 → warning
<!-- /check:index -->
