---
name: map
owner: mapping
consumes: [mapping, trust, tag, index, hot, log]
description: "把 vault/ 中的资产映射为 wiki 代理页：SHA-256、镜像路径、frontmatter、索引/热缓存/日志联动。Triggers on: map, 映射, process this source, add this to the wiki."
---

# map：映射

把 `vault/` 中的资产映射为 `wiki/vault/` 的代理页。登记起步、摘要可选——映射和理解解耦。纯登记动作：只面向已在 vault 的资产，不做任何 vault 侧处理（整理与打磨属 vault 治理，另议）。

## Scope

写：mapping（代理页）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、tag（词表 `wiki/tags.md`）、trust（generated）、vault（原文）

## Steps

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——值集与既有词表在写入前可见
2. 读 vault/ 中目标资产
3. 按注入区写侧契约组装代理页草稿（mapping 镜像与登记字段、trust generated、tag 打标），计算 SHA-256；**呈映射预览**（路径 / 哈希 / 描述 / tags），等用户确认
4. 确认后写代理页；摘要 / 结构抽取为可选增强
5. **写后管道**（确定性，机械自动不询问）：按注入区序执行各插件写入调用（index 重建 → hot → log），毕即 `python .meta/scripts/pipeline.py verify`（写后自证，未过即回修）；随即按提交纪律入库（`map: <资产名>`，见 `.meta/protocol/actions.md`）
6. 回报：路径 / 哈希 / 描述 / tags

## Prohibitions

- 不修改 vault/ 任何文件（命令侧对 vault 只增）
- 代理正文不复制原文全文；日记类资产代理以登记为主，不强制摘要
- 不跳过哈希计算

## Language

生成内容中文为主，英文专名与路径保留原形。

## Parameters

- 资产路径（vault/ 内相对路径）；可批量

## Injected Section (plugin usage blocks)

> 本区为 plugin_cli 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:mapping -->
- 镜像定位：代理路径 = `wiki/vault/<原路径>.md`（原名 + .md，防同名碰撞）；md 资产同样有代理，无特例
- 登记字段：`type: source` + `raw_file`（根相对路径）/ `raw_sha256`（十六进制 SHA-256，不跳过计算）
- 正文一行描述起步，不复制原文全文；摘要 / 结构抽取为可选增强
<!-- /usage:mapping -->

<!-- usage:trust -->
- 写页随手写 `generated`（块式：`by: agent/<当前模型>` / `at: 今日`）
- 复核动作发生时追加 `verified` 事件（单行 `by: <actor>, at: <日期>`），不为凑水位伪造
<!-- /usage:trust -->

<!-- usage:tag -->
- 写入前读 `wiki/tags.md`，优先复用既有词
- 新词规范：中文为主、英文小写 kebab-case、层级 `父/子` ≤2、每页 ≤5、禁复述 type
<!-- /usage:tag -->

<!-- usage:index -->
- 写后重建（机械自动）：`python .meta/scripts/pipeline.py index`（各目录索引）与同脚本 `tags`（tag 反向索引）；LLM 不手写索引
<!-- /usage:index -->

<!-- usage:hot -->
- 写条目（机械自动）：`python .meta/scripts/pipeline.py hot <类型> "<wikilink + 一句话核心>"`；窗口淘汰与截短由脚本执行
<!-- /usage:hot -->

<!-- usage:log -->
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>"`；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
