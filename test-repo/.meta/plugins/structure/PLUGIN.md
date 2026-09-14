# structure：vault 布局

vault 不预设结构，但完全无结构意味着熵的快速增长（user-write 手稿 2026-09-07）。本插件立布局规约：结构由实例声明，框架提供预设菜单、落位规则与漂移检测——骨架（机制）与实例（具体结构）分离。vault 侧自此与 wiki 侧对称：概念插件管「是什么」，结构插件管「怎么组织」。

## Structure

- `wiki/structure.md`——结构声明页（type: structure）：frontmatter `structure` 块映射放声明本体（顶层目录 → 一句话语义，机器可读），正文放预设选择与说明（人读）；页面缺席 = 平铺容忍（合法状态）
- 预设菜单：日期（`xxxx-xx-xx` 每日文件夹）/ 格式（`pdf/`、`md/`）/ 类型（日记、切片等语义分类）/ 混合（嵌套不互斥）
- 外壳自然语言声明退役：wiki 内才是 agent 检索可达区，外壳留指针指向声明页

## Invariants

- 结构选择是实例配置，不进架构——试金石：具体目录布局搬不进新实例
- vault 属人：结构调整自由，agent 只落放与提示，不强制
- 声明与现状的双向 diff 机械可判（附检脚本）；声明是意图，diff 是漂移提示，处置永远属人
- diff 只约束顶层目录；顶层散文件是平铺位，不受声明约束

## Changelog

- 0.2（2026-09-14）领地落 wiki：声明页 `wiki/structure.md`（frontmatter structure 块映射机械可读）；漂移检测自语义项升级附检脚本（声明 diff）；depends 增 wiki；外壳自然语言声明退役
- 0.1（2026-09-14）立设：自 user-write 手稿（四预设 + AGENTS 声明）与 vault 治理讨论蒸馏；布局职责自 vault 概念插件独立，对称于 wiki 侧概念/结构分层
