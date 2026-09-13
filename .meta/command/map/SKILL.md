---
name: map
owner: mapping
consumes: [mapping, trust, user-profile, tag, index, hot, log]
description: "把 vault/ 中的资产映射为 wiki 代理页：SHA-256、镜像路径、frontmatter、索引/热缓存/日志联动。Triggers on: map, 映射, process this source, add this to the wiki."
---

# map：映射

把 `vault/` 中的资产映射为 `wiki/vault/` 的代理页——映射和理解解耦，纯登记动作（登记字段与正文尺度等写侧契约见注入区）。只面向已在 vault 的资产，不做任何 vault 侧处理（整理与打磨属 vault 治理，另议）。

## Scope

写：mapping（代理页）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、tag（词表 `wiki/tags.md`）、trust（generated）、vault（原文）

## Steps

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——值集与既有词表在写入前可见
2. 读 vault/ 中目标资产
3. 按注入区写侧契约组装代理页草稿（mapping 镜像与登记字段、trust generated、tag 打标）；**呈映射预览**（路径 / 哈希 / 描述 / tags），等用户确认
4. 确认后写代理页
5. **写后管道**（确定性，机械自动不询问）：按注入区序执行各插件写入调用，毕即 `python .meta/scripts/pipeline.py verify`（写后自证，未过即回修）；随即按提交纪律入库（`映射: <资产名>`，词表见 `.meta/protocol/actions.md`）
6. 回报：路径 / 哈希 / 描述 / tags

## Prohibitions

- 不修改 vault/ 任何文件（命令侧对 vault 只增）；其余硬规则（哈希必算、正文不复制全文等）以注入区 mapping 块为准

## Language

生成内容中文为主，英文专名与路径保留原形。

## Parameters

- 资产路径（vault/ 内相对路径）；可批量

## Injected Section (plugin usage blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:mapping -->
- 镜像定位：代理路径 = `wiki/vault/<原路径>.md`（原名 + .md，防同名碰撞）；md 资产同样有代理，无特例
- 登记字段：`type: source` + `raw_file`（根相对路径）/ `raw_sha256`（十六进制 SHA-256，不跳过计算）
- 正文一行描述起步，不复制原文全文；摘要 / 结构抽取为可选增强；日记类资产以登记为主，不强制摘要
<!-- /usage:mapping -->

<!-- usage:trust -->
- 写页随手写 `generated`（块式：`by: agent/<当前模型>` / `at: 今日`）
- 复核动作发生时追加 `verified` 事件（单行 `by: <actor>, at: <日期>`），不为凑水位伪造
- 复核由用户发起（人指令触发），agent 不自发追加 verified 事件
<!-- /usage:trust -->

<!-- usage:user-profile -->
- 更新自发触发，双通道：对话保存时观察自述信号（偏好表达、纠正、背景），资产映射时观察行为信号（题材、领域、素材习惯）
- 断言 = 一行主张 + 行内证据 wikilink；单条增量断言不直接升格为偏好，偏好为页内聚合出的模式
- 收敛式更新：新值取代旧值时正文留痕（单行：谁何时改了什么）；整页重写仅限画像建构/整合（独立命令后置，随初始化机制定案）
- 日记类资产只记元信号（有无、节奏），内容不进画像（豁免随 mapping）
- 隐私红线：画像内容是实例数据，不入框架仓库与 test-repo
<!-- /usage:user-profile -->

<!-- usage:tag -->
- 写入前读 `wiki/tags.md`，优先复用既有词
- 新词规范：中文为主、英文小写 kebab-case、层级 `父/子` ≤2、每页 ≤5、禁复述 type
<!-- /usage:tag -->

<!-- usage:index -->
- 写后重建（机械自动）：`python .meta/scripts/pipeline.py index`（各目录索引）与同脚本 `tags`（tag 反向索引）；LLM 不手写索引
<!-- /usage:index -->

<!-- usage:hot -->
- 写条目（机械自动）：`python .meta/scripts/pipeline.py hot <类型> "<wikilink + 一句话核心>"`（类型值集同 log，见 AGENTS 注入区 log 块）；窗口淘汰与截短由脚本执行
<!-- /usage:hot -->

<!-- usage:log -->
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>"`（类型值集见 AGENTS 注入区 log 块）；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
