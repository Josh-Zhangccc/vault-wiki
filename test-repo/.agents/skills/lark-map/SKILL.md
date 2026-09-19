---
name: lark-map
owner: lark
consumes: [lark, lark-docs, lark-im, trust, index, hot, log]
description: "把飞书侧资源映射为 wiki/lark/ 指针页：读 profile 与域声明 → 逐域枚举 lark-cli → diff token 集 → 建/改/标废弃 → 写后管道。Triggers on: lark-map, 拉取飞书, 同步飞书, lark map."
---

# lark-map：外部指针映射

把 lark-cli 可达的飞书资源映射为 `wiki/lark/` 领地页——映射与理解解耦，纯登记与对账动作（指针页契约与档案页分区制见注入区 lark 块）。内容打磨与蒸馏不归本命令（走 save 进 notes / 档案沉淀区）。

## Scope

写：lark（指针页、档案页机械区与域枢纽）、log、hot、index
读：registry（`.meta/protocol/registry.yaml`，字段与值集锚点）、lark 域插件枢纽页（docs.md / im.md 等）、lark-cli（枚举与元数据）

## Steps

1. **锚点（一次读取）**：读 registry 与 `wiki/lark/` 目录集（= profile 清单）及各 `profile.md`（TTL 覆写）
2. 逐 profile × 现役域（域枢纽页在场即现役）执行域对账：
   - docs 域：读 `docs.md` 关心区（`docs` 块映射）→ `lark-cli --profile <名>` 枚举（wiki 空间节点树 / drive 文件树）→ 解析关心区对象集 → 与 `docs/` 指针页 token 集 diff → 新增建页、变更改页（frontmatter 机械字段覆写）、消失标 `status: deprecated`；结构速写过期则重蒸馏并重置 stale_after
   - im 域：读 `im.md` 策略（`im` 块映射）→ `im +chat-list` 全量枚举群 → 与 `im/chats/` 群档 token 集 diff → 新建（群功能 description 蒸馏 + key_members 群主起步）/ 改机械区 / 退群标 `status: deprecated`；**人不枚举**（涌现制，见注入区 lark-im 块）；key_members 追加已建档成员的 wikilink
3. **呈对账预览**（新增 / 变更 / 废弃清单），等用户确认
4. **写后管道**（确定性，机械自动不询问）：`python .meta/scripts/pipeline.py verify`（写后自证，未过即回修）；随即按提交纪律入库（`映射: <profile>/<域>`，词表见 `.meta/protocol/actions.md`）
5. 回报：profile / 域 / 新增 / 变更 / 废弃计数

## Prohibitions

- docs 域全量映射禁——枚举只服务结构速写与关心区解析（以注入区 lark-docs 块为准）
- 档案页正文沉淀区（议题记录、关系）只增不改，本命令不写沉淀区（按需蒸馏属独立动作且须用户确认）
- 发送 / 回复 / 加急等写面操作不属本命令（永远须用户明示）
- CLI 调用必带 `--profile`；auth 状态现查不落盘
- 不碰 notes / sessions 与 `wiki/vault/`（mapping 领地）；快照选段按需、禁全文复制

## Language

生成内容中文为主，英文专名与路径保留原形。

## Parameters

- profile 名（可省 = 全部）；域名（可省 = 全部现役域）

## Injected Section (plugin usage blocks)

> 本区为 wiki_plugin_kernel 自各插件 manifest usage 列表按本命令 consumes 序投影（inject / all 重建）；手写内容不进此区，改写侧契约改 PLUGIN.yaml。

<!-- cmd-inject:start -->
<!-- usage:lark -->
- 指针页登记字段：`type: lark` + `lark` 块映射（profile = 所在目录名、kind = 对象类型、token、url）+ generated / stale_after
- 遇 stale 指针页：带 `--profile` 用 lark-cli 现拉，覆写 frontmatter 机械字段（updated / stale_after），快照类正文追加不覆写
- 新建 profile：`wiki/lark/` 下建目录（名 = cli profile 名）+ `profile.md`（kind: profile，一句话 + 可选 TTL 覆写）；域插件自动覆盖该目录
- 域插件契约：depends lark，遍历全部 profile 目录平行服务，只约束各自 kind 词表与域内页面格式，不碰 profile 抽象
<!-- /usage:lark -->

<!-- usage:lark-docs -->
- 建/改关心区：改 `docs.md` `docs` 块映射（范围一句话：知识空间名 / 云盘目录 / 特定对象），lark-map 或 agent 按区枚举落指针页；关心区即指针页目录段
- 结构速写：wiki 空间清单 + 云盘顶层树蒸馏成一屏（agent 产物），随拉取重置 stale_after；不追求与 lark 侧实时一致
- 指针页正文一行摘要起步；快照节 `## 快照 YYYY-MM-DD` 选段追加、禁全文复制
- kind 词表跟 lark obj_type：docx / wiki / sheet / base / file / …（开放，新词先查 registry）
<!-- /usage:lark-docs -->

<!-- usage:lark-im -->
- 建群档（lark-map 对账）：`im +chat-list` 全量 → token↔页 diff → 新建（群功能 description 蒸馏 + key_members 群主起步）/ 改机械区 / 退群标 deprecated
- 建人档（涌现，命中枢纽条件时手建）：contact 解析填 department / position；有 p2p 填 chat_id 锚；关系区留白起步
- 议题记录（按需）：`chat-messages-list` 拉时间窗 → contact 翻译人名、threads 展开话题楼 → 蒸馏成 `## YYYY-MM-DD 议题：X → 结果：Y` 一节 → 呈用户确认后追加（沉淀区只增）
- 关系更新：新观察追加一行（日期 + 一句话 + 证据 wikilink），旧断言不删改，收敛式靠人裁决
<!-- /usage:lark-im -->

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
- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>"`（类型值集见 AGENTS 注入区 log 块）；滚动窗口与归档由脚本执行
<!-- /usage:log -->
<!-- cmd-inject:end -->
