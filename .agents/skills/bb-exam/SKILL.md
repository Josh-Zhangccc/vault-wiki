---
name: bb-exam
owner: bb-exam
consumes: [bb-exam, bb-track, trust, log]
description: "出题自测：读 bb-track 认知档案与 courseware 知识点，生成英文试题 + 中文解析，题型/难度对齐样例、知识点不越界、解析回链课件位置。Triggers on: 出题, 自测, 测试, 生成习题, exam, quiz."
---

# bb-exam：出题自测

用户指定范围（+ 可选样例），读 bb-track 认知档案知道「哪些点生疏该测、哪些点掌握可挑战」，再按 courseware 知识点生成英文试题 + 中文解析，题型与难度中值对齐样例、知识点绝不越界、解析回链课件位置。定位 = 检验，与 bb-teach（教学）正交；选题/难度/术语/范围规则见注入区。

## Scope

写：exams/（试题.md + 答案.md，exam 块映射 + trust 字段）、log（写后一行）
读：registry（`.meta/protocol/registry.yaml`，字段锚点）、courseware（sm-N + 专有名词）、assessments（已知作业）、user.md（bb-track 认知档案）、sessions（bb-teach 纪要，按需）

## Steps

1. **解析输入**：范围（章节/单元/sm-N 列表）+ 样例（可选）
2. **读知识点全集**：courseware sm-N + `## 专有名词` 对照表，取范围内子集
3. **读用户认知**：user.md 熟练度/目标层/证据流（stale 先核对）
4. **定题型与难度中值**：样例 → assessments 已知作业 → user-profile 习惯
5. **按需读 bb-teach 记录**：近期 session 纪要
6. **选题**：范围内知识点按 生疏/未锚点/错题/短期优先 排序覆盖
7. **出题**：英文、术语对齐、题型对齐、难度围绕中值
8. **写解析**：中文、每题标知识点 + sm-N wikilink
9. **落盘**：exams/<course>/<test-name>-试题.md + -答案.md
10. **写后**：log 行（other --domain bb）+ pipeline.py verify

## Prohibitions

- 绝不出现课程知识范围外或用户指定范围外的知识点（除非用户明示）
- 不改 bb/ 源侧、courseware/assessments 纯代理页
- 试题页不写答案/解析（试题应干净）；答案页不写题干全文
- 隐私：自测卷属实例数据，不入框架仓库

## Language

题目英文（术语对齐 courseware 专有名词表）；解析中文；路径与专名保留原形。

## Parameters

- 范围（章节/单元/知识点，必填）
- 样例（习题/试卷，可选）
- 题量（可选，缺省适中）

## Injected Section (plugin usage blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:bb-exam -->
- 解析输入：范围（章节/单元/sm-N 列表）+ 样例（可选）
- 读知识点全集：courseware sm-N + `## 专有名词` 对照表，取范围内子集
- 读用户认知：user.md 熟练度/目标层/证据流，stale 先核对（纪律见注入区 bb-track 块）
- 定题型与难度中值：样例 → assessments 已知作业 → user-profile 偏好层习惯；难度 = 认知层级 1-5（记忆/理解/应用/分析/综合），中值 M = 样例各题层级中位数
- 按需读 bb-teach 记录：近期 session 纪要（最近教了什么/卡在哪），避免重复或重点测刚教
- 选题：范围内知识点按 生疏/未锚点/错题/短期优先 排序覆盖
- 出题：英文题干、术语对齐 courseware 专有名词表、题型对齐样例、难度围绕 M（生疏偏易、掌握偏难，整体中位数 = M）
- 写解析：中文、每题标知识点 + sm-N wikilink
- 落盘：exams/<course>/<test-name>-试题.md + -答案.md（exam 块映射 + generated + stale_after）
- 不越界：术语/知识点只取自范围内 courseware sm-N，越界弃题重出（除非用户明示）
- 写后：log 行（类型 other --domain bb）+ pipeline.py verify
<!-- /usage:bb-exam -->

<!-- usage:bb-track -->
- 建档：首个显著信号或用户明示时建 user.md（type: bb + generated/updated/stale_after）；缺席即无认知数据，消费侧降级处理不报错
- 追加证据：`- MM-DD 出处（human 对话|machine grades|human 笔记|ai 笔记|human 复核）：断言 → [[回链]]`；出处开放词表
- 收敛读数：新证据到 → 读数行改写（新值取代旧值，行内留最近证据摘要与日期）；证据流不动
- 消费纪律：teaching/testing/复盘类输出前先读 user.md；stale 先核对近窗证据或询问；差距分析 = courseware 知识点全集 − 已锚点集，现算
- 笔记消费：读 notes/ 概览与 stage/origin 属性作信号；不改不删不代标 stage；ai 笔记仅弱证据
- 写后管道：verify；log 行（类型 profile，--domain bb）
- 认知桥注册（user-profile 按需桥）：建档时若画像页在场，维护其 `## 域认知` 节一行 `- bb：wiki/bb/<term>/<course>/user.md`（路径形通配多课多档）；画像缺席跳过不代建（按需桥缺席容错）
<!-- /usage:bb-track -->

<!-- usage:trust -->
- 写页随手写 `generated`（块式：`by: agent/<当前模型>` / `at: 今日`）
- 复核动作发生时追加 `verified` 事件（单行 `by: <actor>, at: <日期>`），不为凑水位伪造
- 复核由用户发起（人指令触发），agent 不自发追加 verified 事件
<!-- /usage:trust -->

<!-- usage:log -->
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>" [--domain 域]`（类型值集见 AGENTS 注入区 log 块；域标 = 域件名如 bb/lark/vault，域内事务必带、框架与原生事务缺省）；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
