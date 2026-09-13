---
name: save
owner: [notes, sessions]
description: "把当前对话、答案或洞见存为 wiki 原生笔记。先去重再落档，推断类型与标题，长会话分块提取，更新索引/日志/热缓存。Triggers on: save this, /save, file this, save to wiki, 保存."
---

# save：沉淀

好答案不该消失在聊天记录里。把刚讨论的内容存为 wiki 永久页。wiki 靠它复利，勤存。

## Scope

写：sessions（会话骨干页）、notes（原生笔记）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、trust（信任字段契约 `.meta/plugins/trust/`，generated 随手写）、sessions（骨干页结构 `.meta/plugins/sessions/`）、tag（词表 `wiki/tags.md`）、index / hot（去重前置）

## Dedup Before Filing (required)

1. 读 wiki/hot.md 与 wiki/index.md 了解近期上下文
2. 按标题与关键概念搜既有页面
3. 已有相关页：更新它而非新建；部分重叠：向用户展示差异，由用户选合并 / 更新 / 新建
4. 确认无覆盖页后才新建

## Type and Destination

type / status 值集以 registry 为准（一次读取锚点，不复抄表）；真歧义才问。落点按 type 分流：qa / concept / comparison / decision / entity 落 `wiki/notes/`；session 走下方长会话段，落 `wiki/sessions/`。source 型不在此列——有 vault 对应物的走 map。

## Workflow

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——type / status 值集与既有词表写入前可见，tags 优先复用既有词
2. 扫描对话，识别高价值内容（非显然的洞见、带理由的决策、费力得出的分析、会被再次引用的对比）；跳过机械问答 / 调试过程 / 已在库内容
3. 定 type（真歧义才问）与标题（歧义或冲突才问）
4. 以陈述句现在时重写：写知识，不写对话
5. 建 `wiki/notes/<标题>.md`：frontmatter（type / title / created / updated / status / tags / related + generated 块式：`by: agent/<当前模型>` / `at: 今日`）+ 正文；session 型改落 `wiki/sessions/` 并按插件契约加 participants（见长会话段）
6. 对话中提到的 wiki 页写入 related 并加 wikilink
7. **写后管道**（确定性，机械自动）：`python .meta/scripts/pipeline.py index` → `tags` → `hot save "<wikilink + 一句话核心>"` → `log save "<一句话>"` → `verify`（写后自证，未过即回修）；毕即按提交纪律入库（`保存: <页标题>`，见 `.meta/protocol/actions.md`）
8. 回报：`Saved as [[标题]] in wiki/notes/`（session 型：`... in wiki/sessions/`）

## Long Sessions (session backbone)

1. 按主题切 3-8 段（不按消息数），合并去机械细节
2. 建 session 骨干页：落点 `wiki/sessions/`、默认命名、骨干页形状、participants（actor 列表）与提升规则均以 sessions 插件为准（`.meta/plugins/sessions/`），此处不复抄
3. 独立高价值主题提升为 `wiki/notes/` 页并从骨干页 wikilink；提升前同样先去重
4. 标题真歧义才问（默认命名见插件规范）

## Writing Rules

陈述句现在时；中文为主；提到的概念 / 页面全部 wikilink；未来会话能冷读此页。

## Parameters

- `/save` 全会话；`/save <主题>` 只存该主题；`--force` 跳过确认（仅无冲突时）
