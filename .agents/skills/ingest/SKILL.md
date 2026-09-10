---
name: ingest
owner: vault
description: "把 vault/ 中的资产登记为 wiki 代理页：SHA-256、镜像路径、frontmatter、索引/热缓存/日志联动。Triggers on: ingest, 摄入, process this source, add this to the wiki."
---

# ingest：摄入

把 `vault/`（VAULT）中的资产转化为 `wiki/vault/` 的代理页。登记起步、摘要可选——摄入和理解解耦。

## 涉及结构

写：vault（代理页）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、trust（信任字段契约 `.meta/plugins/trust/`，generated 随手写）、tag（词表 `wiki/tags.md`）、vault（VAULT 原文）

## 步骤

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——值集与既有词表在写入前可见；tags 优先复用既有词
2. 读 vault/ 中目标资产；询问：「需要打磨原始文件吗（添加 frontmatter、清理格式、重命名）？」（日记免问）。打磨走派生副本：产出为新文件（VAULT 只增），不改既有文件
3. 计算 SHA-256；按镜像规则定位代理路径：`wiki/vault/<原路径>.md`（原名 + .md，防碰撞）
4. 组装代理页草稿（frontmatter：`type: source` + created / updated / status（值集内）+ raw_file / raw_sha256 / tags + generated（块式：`by: agent/<当前模型>` / `at: 今日`）；正文一行描述起步），**呈摄入预览**（路径 / 哈希 / 描述 / tags），等用户确认
5. 确认后写代理页；摘要 / 结构抽取为可选增强
6. **写后管道**（确定性，机械自动不询问）：`python .meta/scripts/pipeline.py index` → `tags` → `hot 摄入 "<wikilink + 一句话核心>"` → `log 摄入 "<一句话>"` → `verify`（写后自证，未过即回修）
7. 回报：路径 / 哈希 / 描述 / tags

## 禁止

- 不修改 vault/ 任何既有文件（命令侧对 VAULT 只增；打磨产出为新副本）
- 代理正文不复制原文全文；日记类资产代理以登记为主，不强制摘要
- 不跳过哈希计算

## 语言

生成内容中文为主，英文专名与路径保留原形。

## 参数

- 资产路径（vault/ 内相对路径）；可批量
