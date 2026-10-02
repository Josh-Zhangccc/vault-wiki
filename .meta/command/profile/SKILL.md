---
name: profile
owner: user-profile
consumes: [user-profile, trust, index, hot, log]
description: "维护用户画像 wiki/profile.md：识别自述与行为信号，收敛式更新断言（新值取代旧值、正文留痕、证据 wikilink），建构与整合走整页重写预览。Triggers on: profile, 更新画像, 画像更新, update profile."
---

# profile：画像更新

把对使用者的持续认知写成可检查的页面：断言带证据、偏好会过期、更新留痕。方向是「内 → 用户认知」——与 map（外 → 内翻译）、save（会话落盘）正交；收敛式跨 session，非事务性一次完成。写侧契约（信号判据、分层落点、断言格式、收敛留痕）见注入区。

## Scope

写：user-profile（wiki/profile.md）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、trust（generated / stale_after）、画像现状页（可缺）

## Steps

1. **锚点（一次读取）**：读 `.meta/protocol/registry.yaml` 与 `wiki/profile.md`——缺页 = 首建（建构），不依赖初始化机制
2. **判信号**（判据见注入区）：本会话与近期观察不够格即回报退出，不硬写
3. 组装更新：增量断言（新值取代旧值 + 正文留痕）或建构 / 整合（整页重写）——建构与整合**呈画像预览**（断言 / 证据 / 层次），等用户确认
4. 写页（分层落点、stale_after 续期见注入区）
5. **写后管道**（确定性，机械自动不询问）：按注入区序执行各插件写入调用，毕即 `python .meta/scripts/pipeline.py verify`（写后自证，未过即回修）；随即按提交纪律入库（`画像: <一句话>`，词表见 `.meta/protocol/actions.md`）
6. 回报：更新了什么 / 证据链 / 落在哪层

## Prohibitions

- 隐私红线：画像内容是实例数据，不入框架仓库与 test-repo
- 日记类资产只记元信号（有无、节奏），内容不进画像
- 证据页（会话页 / vault 代理页 / lark 档案页）只读引用，不改写

## Language

生成内容中文为主，英文专名与路径保留原形。

## Parameters

- 无参：判定近期信号并更新；`<主题>`：只处理该主题的断言

## Injected Section (plugin usage blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:user-profile -->
- 触发双轨：用户明示 profile；agent 在任意会话识别显著信号后自发调用——信号沉淀统一走本命令，不寄生其他命令流程
- 信号判据：自述信号（偏好表达、纠正、背景）与行为信号（题材、领域、素材习惯）；只记反复出现的题材/领域、显式偏好表达、对输出的纠正、稳定的背景事实（身份/工具/环境）；一次性、工具性内容与不确定的观察不记
- 证据域：wiki 内页面皆可（会话页、vault 代理页、lark 档案页、notes）——引用即 wikilink，跨域不立依赖
- 分层落点：不变的身份事实入静态层；会漂移的兴趣与习惯入动态层并挂 stale_after（随观察续期）
- 断言 = 一行具体可证的主张 + 行内证据 wikilink（「偏好中文简洁回复」优于「喜欢简洁」）；单条增量断言不直接升格为偏好，偏好为页内聚合出的模式
- 收敛式更新：新值取代旧值时正文留痕（单行：谁何时改了什么）；整页重写仅限画像建构/整合（呈预览等确认）
- 首建：首次触发即自建页面（frontmatter：type: profile + generated，动态层挂 stale_after），不依赖初始化机制
- 日记类资产只记元信号（有无、节奏），内容不进画像（豁免随 mapping）
- 隐私红线：画像内容是实例数据，不入框架仓库与 test-repo
<!-- /usage:user-profile -->

<!-- usage:trust -->
- 写页随手写 `generated`（块式：`by: agent/<当前模型>` / `at: 今日`）
- 复核动作发生时追加 `verified` 事件（单行 `by: <actor>, at: <日期>`），不为凑水位伪造
- 复核由用户发起（人指令触发），agent 不自发追加 verified 事件
<!-- /usage:trust -->

<!-- usage:index -->
- 写后重建（机械自动）：`python .meta/scripts/pipeline.py index`（索引——溢出减负制，含并回后多余旧索引删除）与同脚本 `tags`（tag 反向索引）；LLM 不手写索引
<!-- /usage:index -->

<!-- usage:hot -->
- 写条目（机械自动）：`python .meta/scripts/pipeline.py hot <类型> "<wikilink + 一句话核心>"`（类型值集同 log，见 AGENTS 注入区 log 块）；窗口淘汰与截短由脚本执行
<!-- /usage:hot -->

<!-- usage:log -->
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>" [--domain 域]`（类型值集见 AGENTS 注入区 log 块；域标 = 域件名如 bb/lark/vault，域内事务必带、框架与原生事务缺省）；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
