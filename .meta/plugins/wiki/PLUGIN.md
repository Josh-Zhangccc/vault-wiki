# wiki：md 世界（概念）

产品名的另一半：wiki 是 VAULT 在 md 世界的投影与原生知识之总集——agent 与人的公共语言层。本插件是概念声明：只阐述 wiki 是什么、页面出身如何判定，不拥有具体领地（那是 notes / sessions / mapping 的事）、字段、命令或脚本。

## Structure

容器 `wiki/`，区划出身二分：

- 代理页（`wiki/vault/**`）：有 VAULT 对应物，归 mapping 插件
- 原生页（其余）：出身就在 wiki，归 notes / sessions 插件
- 派生页（index / tags / hot / log）：机械投影，归各派生插件

## Invariants

- 路径即出身证明：判定一页是什么，先看它在哪（上述三区），再看 frontmatter
- 库内一切文本 UTF-8、知识页 type 必填、保留名豁免——格式契约 OKF 权威定义见 `docs/01-okf.md`（v0.2），本插件是其实例侧锚点

## Checks

无附检；OKF 合规检查散在各插件（type 值集由 check 底座查、保留名由 index / log 插件实现）。

## Inject

AGENTS.md 一行：wiki 容器语义与出身二分。

## Attachments

无。

## Changelog

- 0.1（2026-09-12）立设：概念声明插件（出身二分不变量自原 vault 插件 PLUGIN.md 移籍）
