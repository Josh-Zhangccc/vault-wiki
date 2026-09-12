# vault-wiki

**个人自用的 agent 知识库框架**：vault 容纳真实资产，wiki 做 md 代理与原生笔记，agent 按 SASU-L 披露顺序零先验读写。md + 纯文件是底座，Obsidian 等仅为可替换 viewer。

> 状态：原型已冻结（2026-09-08~12 构建，两轮真实操作 + 冷启动披露审计通过），当前阶段为日常使用、边用边改。2026-09-12 裁定定位个人自用，普世化与矩阵化测试搁置（沿革见 `log.md`）。

## 它做什么

让 AI 编程助手（agent）替你经营一座「个人维基」：

- 资产放进 `vault/`（任意格式：md / txt / csv / pdf / 图像……），**摄入**命令登记为 `wiki/vault/` 下的 md 代理页（SHA-256 + 元数据 + 链接）
- 对话中的洞见与决策，**保存**命令沉淀为 `wiki/notes/` 原生笔记；会话骨干页入 `wiki/sessions/`
- **检索**命令先读热缓存与索引再综合回答，产出带 wikilink 引用的答案
- 索引 / 标签 / 热缓存 / 运行日志全为派生层自动维护；**检查**命令审计库健康，**插件**命令装卸结构插件

## 核心概念

| 概念 | 定义 |
|---|---|
| VAULT | 真实资产仓库；命令侧只增，删改自由属于人 |
| wiki | VAULT 的 md 代理层 + 原生笔记区 + 派生层（index / tags / hot / log） |
| OKF | md 知识库格式契约（`docs/01-okf.md`，v0.2）：页面与文件结构的权威定义，使 agent 零先验读写 |
| SASU-L | 披露范式：agent 只经 system prompt → AGENTS.md → Skills → 用户原话 → loop 获知信息 |

## 布局

| 目录 | 内容 |
|------|------|
| `.meta/` | 原型核心：九插件三层（origin/field/derived）、五命令主本、协议工件（registry / actions / experiments）、机械脚本（plugin_cli / pipeline / wikilib，纯标准库零依赖） |
| `wiki/`、`vault/` | 数据区（空种子，待真实内容） |
| `.agents/skills/` | 命令部署副本 |
| `user-write/` | 用户手稿（agent 只读） |
| `docs/` | `00-principles.md` 历史设计档案；`01-okf.md` OKF 契约权威定义 |

## 上手

前提：Python 3（纯标准库，无需安装依赖）、git、能读 AGENTS.md 与 skills 的 agent 环境（如 ZCode）；Obsidian 可选，仅作 viewer。

在仓库根打开 agent 会话即可——AGENTS.md 是宪法（含插件注入区），五个命令以自然语言触发：**摄入 / 保存 / 检索 / 检查 / 插件**（主本见 `.meta/command/`）。把文件放进 `vault/`，对 agent 说「摄入」，就是第一次使用。

## 文档指针

- `AGENTS.md` — 宪法与准则（agent 先读）
- `log.md` — 工程日志：现状、阶段、过往操作
- `docs/01-okf.md` — OKF 格式契约（v0.2）
- `.meta/protocol/` — 字段注册表、动作纪律、披露范式
- `user-write/` — 设计初衷与插件规范草案（只读）

## 沿革

2026-08-26 以个人库结构副本起建，08-28 重定位为本工程，09-08 起「插件 + 命令」原型直接落地、经真实操作验证后冻结为现状。设计谱系讨论存于个人库（见 AGENTS.md 指针）。
