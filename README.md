# vault-wiki（工程暂名）

**个人自用的 agent 知识库框架：vault 容纳真实资产，wiki 做 md 代理与原生笔记，agent 按 SASU-L 披露顺序零先验操作。** 2026-09-12 裁定定位个人自用、边用边改（普世化与矩阵化测试搁置，见 `log.md`）。

- 前身：2026-08-26 个人库结构副本，2026-08-28 重定位为本工程；2026-09-08 起「插件 + 命令」原型直接落地，两轮真实操作验证后冻结为现状。
- 核心定义：**vault** = 把任意格式信息存为资产的容器（命令侧只增，删改自由属于人）；**wiki** = 信息 → md 的管道（代理层 `wiki/vault/` + 原生区 `wiki/notes/`、`wiki/sessions/` + 派生层 index/tags/hot/log）；个性化是动态内容，不进架构。

## 布局

| 目录 | 内容 |
|------|------|
| `.meta/` | 原型核心：九插件三层（origin/field/derived）、五命令主本、协议工件（registry/actions/experiments）、机械脚本（plugin_cli/pipeline/wikilib） |
| `wiki/`、`vault/` | 数据区（当前含首轮虚构库「雾港」实验数据） |
| `.agents/skills/` | 命令部署副本 |
| `user-write/` | 用户手稿（agent 只读） |
| `docs/` | 历史设计档案（规范蒸馏时归并） |

宪法与准则见 `AGENTS.md`；项目现状、阶段与日志见 `log.md`。
