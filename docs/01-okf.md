# OKF：md 知识库格式契约（v0.2）

> OKF 约定 md + 纯文件知识库的页面与文件契约，使 agent 与工具能对同一库零先验读写。本文是 OKF 的**首次成文**（2026-09-12）：v0.2 蒸馏自本工程 2026-09-10 的对齐落地（`wiki/log.md` 当日条目）——此前规范仅以会商口径存在、未落文字，本文即为权威定义。缩写沿用工程内名称，全称未定（由所有者补记）。修订 = 协议级变更：过 check、用户裁定、根索引 `okf_version` 随版本更新。

## 定位与边界

- **底座独立**：只约 md 文件与目录结构，不绑定任何工具——Obsidian、WebUI 等均为可替换 viewer
- **实例无关**：守本契约的库即 OKF 库；本工程（vault-wiki）为参考实例
- **分层**：OKF 只管跨实例可移植的核心契约；实例注册表（本工程为 `.meta/protocol/registry.yaml`）是其字段层投影——值集在实例侧封闭扩展，OKF 不枚举笔记类型（type 值集由实例定义）

## 页面两类

- **知识页**：承载概念内容的 md 页（人写或命令写）
- **结构页**：管道拥有的机械页（索引、日志等）——非概念内容，豁免知识页义务

## MUST（硬性）

1. **UTF-8**：库内一切文本文件 UTF-8 编码
2. **type 必填**：知识页 frontmatter 必有 `type`；值集由实例注册表定义并封闭于生产侧（导入/消费侧容忍未知 type）
3. **保留名豁免**：保留名文件（`index.md`、`log.md`）为结构页，豁免 frontmatter 义务（豁免 = 不要求，非禁止——根索引即带 frontmatter）

## SHOULD（约定）

- **版本自述**：根 `index.md` frontmatter 记 `okf_version`，声明库遵循的契约版本
- **渐进披露**：每目录一份 `index.md`，只聚合本层（顶层概念 + 子目录入口），检索逐层下钻
- **描述字段**：知识页推荐 `description`（一句话 ≤80 字），缺失时索引取正文首句
- **生命周期**：`status` 三值 draft / stable / deprecated；deprecated = 为链接与历史保留、已非当前
- **断链语义**：wikilink 指向未写下页面 = warning 级（尚未写下的知识，非错误）
- **日志形状**：`log.md` 置顶追加、条目不改写；超限按月归档，归档文件沿用保留名

## 署名与信任（v0.2 固化）

- **actor 统一格式**（一切署名字段）：`human:名字`（如 human:Joss）/ `process:流程名`（如 process:hash-recalc）/ `agent/模型标识`（如 agent/GLM-5.3）
- **信任四字段**（页面可选）：`generated`（块式 by/at，页面由谁生成）、`verified`（事件列表，项单行 `by: <actor>, at: <日期>`，只追加）、`stale_after`（YYYY-MM-DD 绝对时刻，过期 = now ≥ 该值的纯比较）、`sources`（来源与可信度信号列表）
- **水位推导不落盘**：无记录 = unverified；仅 agent/process = machine-confirmed；含 human = human-reviewed（最高）；过 stale_after = stale（覆盖显示）——消费方读取时现算，可再生区不造第二份会漂移的真相

## 与本工程的对齐点（实例投影索引）

- 字段与值集 → `.meta/protocol/registry.yaml`（权威源为其 protocol 段）
- 保留名与豁免实现 → index / log 插件 PLUGIN.md
- 信任字段实现与样例 → trust 插件 PLUGIN.md
- 断链与链接语法 → link 插件 PLUGIN.md

## 版本记录

- 0.2（2026-09-12 成文）：三 MUST、保留名、okf_version、渐进披露、description、status 三值、断链语义、日志形状、actor 约定、信任四字段与水位推导——全部蒸馏自 2026-09-10 对齐落地的实现现状，成文与实现对齐无超前
