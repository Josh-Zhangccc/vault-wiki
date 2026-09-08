---
name: ingest
description: "把 vault/ 中的资产登记为 wiki 代理页：SHA-256、镜像路径、frontmatter、索引/热缓存/日志联动。Triggers on: ingest, 摄入, process this source, add this to the wiki."
---

# ingest：摄入

把 `vault/`（VAULT）中的资产转化为 `wiki/vault/` 的代理页。登记起步、摘要可选——摄入和理解解耦。

## 涉及结构

写：vault（代理页）、log、hot、index
读：tag（字段规范）、vault（VAULT 原文）

## 步骤

1. 读 vault/ 中目标资产；询问：「需要打磨原始文件吗（添加 frontmatter、清理格式、重命名）？」（日记免问）
2. 计算 SHA-256
3. 按镜像规则定位代理路径：`wiki/vault/<原路径>.md`（原名 + .md，防碰撞）
4. 写代理页：
   - frontmatter：`type: source` + created / updated / status（协议字段）、raw_file、raw_sha256（vault 插件字段）、tags（tag 插件字段）
   - 正文：一行描述起步；摘要 / 结构抽取为可选增强
5. 重建 wiki/index.md 与 wiki/tags.md（index 插件：只整体重建，不增量写）
6. wiki/hot.md 置顶加条目（最近摄入节）
7. wiki/log.md 置顶追加一行（类型「摄入」）
8. 呈预览（路径 / 哈希 / 描述 / tags），确认后收尾

## 禁止

- 不修改 vault/ 任何既有文件（命令侧对 VAULT 只增）
- 代理正文不复制原文全文
- 不跳过哈希计算

## 语言

生成内容中文为主，英文专名与路径保留原形。

## 参数

- 资产路径（vault/ 内相对路径）；可批量
