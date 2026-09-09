---
name: save
description: "把当前对话、答案或洞见存为 wiki 原生笔记。先去重再落档，推断类型与标题，长会话分块提取，更新索引/日志/热缓存。Triggers on: save this, /save, file this, save to wiki, 保存."
---

# save：沉淀

好答案不该消失在聊天记录里。把刚讨论的内容存为 wiki 永久页。wiki 靠它复利，勤存。

## 涉及结构

写：notes（原生笔记）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、tag（词表 `wiki/tags.md`）、index / hot（去重前置）

## 落档前去重（必做）

1. 读 wiki/hot.md 与 wiki/index.md 了解近期上下文
2. 按标题与关键概念搜既有页面
3. 已有相关页：更新它而非新建；部分重叠：向用户展示差异，由用户选合并 / 更新 / 新建
4. 确认无覆盖页后才新建

## 类型裁决

| type | 用于 |
|------|------|
| qa | 具体问题及其答案 |
| concept | 解释或定义一个概念 / 模式 / 框架 |
| comparison | 并排对比 |
| decision | 架构 / 项目 / 战略决策 |
| session | 完整会话摘要（骨干页） |
| entity | 人物 / 组织 / 产品等实体页 |

类型集以 registry 值集为准（上表为建议项）；status 取值 seed / developing / done。

统一落 `wiki/notes/`，细分靠 type 字段，不靠目录。source 型不在此列——有 VAULT 对应物的走 ingest。

## 工作流

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——type / status 值集与既有词表写入前可见，tags 优先复用既有词
2. 扫描对话，识别高价值内容（非显然的洞见、带理由的决策、费力得出的分析、会被再次引用的对比）；跳过机械问答 / 调试过程 / 已在库内容
3. 定 type（真歧义才问）与标题（歧义或冲突才问）
4. 以陈述句现在时重写：写知识，不写对话
5. 建 `wiki/notes/<标题>.md`：frontmatter（type / title / created / updated / status / tags / related）+ 正文
6. 对话中提到的 wiki 页写入 related 并加 wikilink
7. 重建 wiki/index.md 与 wiki/tags.md
8. wiki/log.md 置顶追加（类型「保存」，超 100 条先归档分流）；wiki/hot.md 先淘汰越界再置顶更新
9. 回报：`Saved as [[标题]] in wiki/notes/`

## 长会话（分块提取）

1. 按主题切 3-8 段（不按消息数）
2. 每段提取：核心结论 / 决策与理由 / 非显然洞见 / 开放问题 / 相关页
3. 合并、去机械细节；建一个 session 骨干页；把独立高价值主题提升为单独页面并从骨干页链接
4. 提升前同样先去重
5. 默认标题 `YYYY-MM-DD-<主题>`；冲突或过泛才问

## 写作规范

陈述句现在时；中文为主；提到的概念 / 页面全部 wikilink；未来会话能冷读此页。

## 参数

- `/save` 全会话；`/save <主题>` 只存该主题；`--force` 跳过确认（仅无冲突时）
