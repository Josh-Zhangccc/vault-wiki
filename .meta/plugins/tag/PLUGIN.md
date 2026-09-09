# tag：语义分类

跨全部页面的分类体系。语义工作在写入时完成（摄入/保存时顺手打标），检索时只做机械匹配——tag 是零基础设施的语义索引。

## 结构（无 wiki 自有文件）

拥有 `tags` 字段规范：

- YAML 列表；中文为主，英文专名保留原形
- 英文 tag 用小写 kebab-case（如 local-llm）
- 层级允许 `父/子` 形式，深度 ≤2
- 每页 ≤5（软上限）

## 不变量

- `type` 是协议封闭枚举（出身，给机器读）；`tags` 是开放语义分类（给人/agent 检索），禁止复述 type 语义
- 词表自由生长，治理靠事后合并，不做前置受控

## 检查（注入 check）

- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：单页 >5 个 tag → warning；tags 复述 type → warning
- 语义项（check 命令）：近重复 tag → warning 提示合并，合并由人执行

## 注入

AGENTS.md 一行：tags 字段规范要点。

## 附件

无 wiki 附件；附检脚本 `scripts/check.py`（机械检查项，audit 发现式执行）。

## 变更记录

- 0.1（2026-09-08）新立，吸收原 lint 近重复检查思想
- 0.2（2026-09-09）机械检查项落为附检脚本（scripts/check.py），本文件保留语义项
