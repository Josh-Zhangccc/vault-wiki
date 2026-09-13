# wiki：md 世界（概念）

产品名的另一半：wiki 是 VAULT 在 md 世界的投影与原生知识之总集——agent 与人的公共语言层。本插件是概念声明：只阐述 wiki 是什么、页面出身如何判定，不拥有领地、字段、命令或脚本。

## Structure

容器 `wiki/`，区划出身二分：

- 代理页（`wiki/vault/**`）：有 VAULT 对应物
- 原生页（其余）：出身就在 wiki
- 派生页（index / tags / hot / log）：机械投影

## Invariants

- 路径即出身证明：判定一页是什么，先看它在哪（上述三区），再看 frontmatter
- 库内一切文本 UTF-8、知识页 type 必填、保留名豁免

## Checks

无附检。

## Inject

AGENTS.md 一行：wiki 容器语义与出身二分。

## Attachments

无。

## Changelog

- 0.2（2026-09-13）纯化：删「归 X 插件」反向引用与锚点虚衔，区划按出身自足陈述
- 0.1（2026-09-12）立设：概念声明插件（出身二分不变量自原 vault 插件 PLUGIN.md 移籍）
