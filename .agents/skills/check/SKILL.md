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
写：wiki/log.md 一行（类型「检查」）

## 步骤

1. **底座硬检查**（协议级，固定清单）：
   - 每个 `.meta/plugins/<id>/` 有 PLUGIN.yaml 与 PLUGIN.md
   - manifest 五字段齐全（id / version / depends / updated / attachment）；id 与目录名一致；depends 指向存在的插件
   - AGENTS.md 注入区标记块与插件集双向一致：多块 = 幽灵，少块 = 未注入
   - `.agents/skills/<name>/SKILL.md` 与 `.meta/command/<name>/SKILL.md` 逐字一致（漂移）
   - `.meta/command/` 每个 SKILL.md 有 frontmatter（name / description）
2. **插件检查**：逐插件执行下方注入区的检查块
3. **语义检查**：读插件与命令文件，查悬挂引用（命令涉及不存在的结构）、幽灵字段（页面 frontmatter 字段无拥有插件）、注入区块与 PLUGIN.md 检查节不一致
4. 汇总输出：PASS / WARN / FAIL 计数 + 分级明细
5. wiki/log.md 置顶追加一行（类型「检查」）
6. 询问是否修复可修复项（重建索引、重部署副本）；不自动改历史条目

## 工具

grep / 读文件即够；脚本可后置（模板仓库提交 959f353 留有可复活的原型）。

## 参数

- 无：全库审计
- 插件 id：只查该插件

## 注入区（各插件检查块）

<!-- check:vault -->
- 镜像 diff：vault/ 有文件无代理 → warning（待登记）；代理无 VAULT 对应物 → error
- raw_sha256 与实际哈希失配 → warning（报告，人决重摄入或删）；代理复制原文全文 → error；无一行描述 → warning
<!-- /check:vault -->

<!-- check:log -->
- 历史条目被修改（git 可核）→ error；无日期条目 → error；容量超限 → warning
<!-- /check:log -->

<!-- check:hot -->
- 窗口越界（超 25 条或超 5 日）→ warning；与 log 矛盾 → warning
<!-- /check:hot -->

<!-- check:tag -->
- 近重复 tag → warning 提示合并；单页 >5 → warning；复述 type → warning
<!-- /check:tag -->

<!-- check:notes -->
- 笔记被命令覆盖痕迹 → error；孤儿笔记（无入链无引用）→ warning；近似重复（Jaccard > 0.7）→ warning
<!-- /check:notes -->

<!-- check:index -->
- 索引与实际页面集偏差 → error（重建即修复）；手编痕迹 → warning
<!-- /check:index -->
