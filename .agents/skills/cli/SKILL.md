---
name: cli
owner: framework
description: "plugin_cli.py 机械核心使用参考：七个子命令（ls/validate/audit/inject/registry/deploy/all）、典型场景与边界。Triggers on: cli, CLI 用法, plugin_cli, 注入块更新, 投影重建, 更新注入."
---

# cli：机械核心使用参考

`python .meta/scripts/plugin_cli.py <子命令>`——框架侧唯一投影机：PLUGIN.yaml 是本体，AGENTS 注入区、check 检查块、命令用法块、注册表插件段、命令副本全是它的投影。幂等，随时可跑，漂移即修复。

## 子命令

| 子命令 | 作用 | 写盘 |
|---|---|---|
| `ls` | 插件清单 + 依赖 + 驱动命令 | 无 |
| `validate` | 合规检查：manifest 字段、依赖无环、owner×commands 双向一致、consumes 在场且带 usage 列表；错误退出码 1 | 无 |
| `audit` | 附检：发现式执行各插件 `scripts/check.py`，只读报告（可带插件 id 只查一个） | 无 |
| `inject` | 重建三种投影：AGENTS 注入区 + check 检查块 + 命令用法块 | AGENTS.md、含注入区的命令 SKILL.md |
| `registry` | 重建 registry.yaml 插件段（自各 manifest `fields`） | registry.yaml |
| `deploy` | 同步命令主本 → `.agents/skills/` 副本；孤儿副本仅报告（删除属人） | 副本 |
| `all` | validate + inject + registry + deploy 一步到位 | 以上全部 |

## 典型场景

- **改了 PLUGIN.yaml**（inject / checks / usage / fields / 版本）：`python .meta/scripts/plugin_cli.py all`——日常标准动作，一条命令全部收敛；validate 不过则阻断，修完重跑
- **只刷注入块**：`inject` 够用，但注意它改的是 `.meta/command/` 主本，副本须 `deploy` 才同步——所以日常一律用 `all`
- **健康快检**：`validate`（结构）+ `audit`（附检）；完整审计（含语义项）走 check 命令
- **装卸插件**：语义流程（决策、目录归档、log 行）走 plugin 命令；其中的机械步骤即本 CLI 的 `validate` / `all` / `audit`

## 边界

- 脚本只碰四处：插件目录进出、注入区标记块、registry 插件段、命令副本；protocol / reserved 段与 AGENTS.md 手写区永不动
- 纯标准库零依赖（Python 3）；中文输出
- 数据区派生层（`wiki/index.md`、`tags.md`、`hot.md`、`log.md`）不归本 CLI——那是 `pipeline.py`（`index` / `tags` / `hot` / `log` / `verify`），由 map / save 的写后管道调用

## Parameters

- 子命令（见上表）；`audit` 可带插件 id
