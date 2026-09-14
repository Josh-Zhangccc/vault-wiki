---
name: save
owner: [notes, sessions]
consumes: [notes, sessions, trust, user-profile, index, hot, log]
description: "把当前对话、答案或洞见存为 wiki 原生笔记。先去重再落档，推断类型与标题，长会话分块提取，更新索引/日志/热缓存。Triggers on: save this, /save, file this, save to wiki, 保存."
---

# save：沉淀

好答案不该消失在聊天记录里。把刚讨论的内容存为 wiki 永久页。wiki 靠它复利，勤存。

## Scope

写：sessions（会话骨干页）、notes（原生笔记）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、tag（词表 `wiki/tags.md`）、trust（generated）、index / hot（去重前置）

## Dedup Before Filing (required)

1. 读 wiki/hot.md 与 wiki/index.md 了解近期上下文
2. 按标题与关键概念搜既有页面
3. 已有相关页：不直接改写——展示差异由用户裁决（追加式并入须用户指令并留痕，或人手改，或另立新页）；部分重叠：同上展示差异由用户选
4. 确认无覆盖页后才新建

## Type and Destination

type / status 值集以 registry 为准（一次读取锚点，不复抄表）；真歧义才问。落点按 type 分流：session 走下方长会话段，其余原生型落 `wiki/notes/`（各型落点与契约见注入区）；source 型不在此列——有 vault 对应物的走 map。

## Workflow

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/tags.md`——type / status 值集与既有词表写入前可见
2. 扫描对话，识别高价值内容（非显然的洞见、带理由的决策、费力得出的分析、会被再次引用的对比）；跳过机械问答 / 调试过程 / 已在库内容
3. 定 type（真歧义才问）与标题（歧义或冲突才问）
4. 以陈述句现在时重写：写知识，不写对话
5. 按注入区写侧契约建页（notes / sessions 落点与形状、trust generated、tag 打标）；session 型走长会话段
6. 对话中提到的 wiki 页写入 related 并加 wikilink
7. **写后管道**（确定性，机械自动）：按注入区序执行各插件写入调用，毕即 `python .meta/scripts/pipeline.py verify`（写后自证，未过即回修）；随即按提交纪律入库（`保存: <页标题>`，见 `.meta/protocol/actions.md`）
8. 回报：`Saved as [[标题]] in wiki/notes/`（session 型：`... in wiki/sessions/`）

## Long Sessions (session backbone)

1. 按主题切 3-8 段（不按消息数），合并去机械细节
2. 建 session 骨干页：落点、默认命名、participants、骨干页形状与提升规则见注入区 sessions 块
3. 标题真歧义才问

## Writing Rules

陈述句现在时；中文为主；提到的概念 / 页面全部 wikilink；未来会话能冷读此页。

## Parameters

- `/save` 全会话；`/save <主题>` 只存该主题；`--force` 跳过确认（仅无冲突时）

## Injected Section (plugin usage blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:notes -->
- 落点 `wiki/notes/<标题>.md`，文件名自由（人起名）；type 形态词表见 registry（开放自扩），领地值不落本区
- 只增：命令不整页重写既有笔记；更新 = 用户指令下的追加式并入（正文留痕）或人手改
<!-- /usage:notes -->

<!-- usage:sessions -->
- 落点 `wiki/sessions/YYYY-MM-DD-<主题>.md`（默认命名），type: session，participants 必填（actor 列表）
- 骨干页五节形状：核心结论 / 决策与理由 / 非显然洞见 / 开放问题 / 相关页（全形状样例见 `.meta/plugins/sessions/PLUGIN.md` Example 节）
- 独立高价值主题提升为 `wiki/notes/` 页，骨干页留 wikilink；提升前先去重
<!-- /usage:sessions -->

<!-- usage:trust -->
- 写页随手写 `generated`（块式：`by: agent/<当前模型>` / `at: 今日`）
- 复核动作发生时追加 `verified` 事件（单行 `by: <actor>, at: <日期>`），不为凑水位伪造
- 复核由用户发起（人指令触发），agent 不自发追加 verified 事件
<!-- /usage:trust -->

<!-- usage:user-profile -->
- 更新自发触发，双通道：对话保存时观察自述信号（偏好表达、纠正、背景），资产映射时观察行为信号（题材、领域、素材习惯）
- 信号判据：只记反复出现的题材/领域、显式偏好表达、对输出的纠正、稳定的背景事实（身份/工具/环境）；一次性、工具性内容与不确定的观察不记
- 分层落点：不变的身份事实入静态层；会漂移的兴趣与习惯入动态层并挂 stale_after（随观察续期）
- 断言 = 一行具体可证的主张 + 行内证据 wikilink（「偏好中文简洁回复」优于「喜欢简洁」）；单条增量断言不直接升格为偏好，偏好为页内聚合出的模式
- 收敛式更新：新值取代旧值时正文留痕（单行：谁何时改了什么）；整页重写仅限画像建构/整合（独立命令后置，随初始化机制定案）
- 日记类资产只记元信号（有无、节奏），内容不进画像（豁免随 mapping）
- 隐私红线：画像内容是实例数据，不入框架仓库与 test-repo
<!-- /usage:user-profile -->

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
