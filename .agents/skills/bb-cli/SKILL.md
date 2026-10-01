---
name: bb-cli
owner: framework
description: "从 bb.cuhk.edu.cn（CUHK-SZ Blackboard）只读拉取课程/作业/成绩/公告/课件/提交并转述，经 connectors/bb-cli 查询，不落 wiki。Triggers on: bb-cli, bb, blackboard, bb.cuhk.edu.cn, 从 bb 获取, 查 bb 课程, 查 bb 作业, 查 bb 成绩, 查 bb 公告."
---

# bb-cli：Blackboard 只读连接器

用 `connectors/bb-cli/`（纯只读 CLI 数据面）从 bb.cuhk.edu.cn 拉取信息并转述。查询即回答，不落 wiki、不改任何数据区。

## Scope

读：Blackboard（课程 / 作业 / 成绩 / 公告 / 课件 / 我的提交 / 成员）
写：无（只读；提交作业、发公告等写操作刻意不提供，需用户明示并另行设计）

## 前置（安装 / 认证）

1. 安装（未装时）：`cd connectors/bb-cli && python3 -m pip install --user --break-system-packages -e .`（依赖仅 curl_cffi + beautifulsoup4；本机已装 0.1.3，也可按 README 走 `.venv`）
2. 登录：`bb-cli login --username <学号> --no-store`（密码经 `BB_CLI_PASSWORD` 环境变量或交互录入；`--no-store` 不落盘，会话 cookie 存 `~/.bb-cli/session.json`）
3. 自检：`bb-cli status --format text` → `authenticated=yes` 即就绪；401 时重 `login`

## Steps

1. `bb-cli status` 确认会话
2. 按需求选命令查询（见「命令速查」）；`--format text` 人读一行一条，JSON 保留 API 原值
3. 把结果转述成中文给用户

## 命令速查

| 需求 | 命令 |
|---|---|
| 我的课程 | `bb-cli courses [--term 学期名子串] --format text` |
| 学期表 | `bb-cli terms --format text`（先定位当前学期名，再 `courses --term` 过滤，如 `--term 2610UG`） |
| 作业+完成情况 | `bb-cli assignments <课程> --format json`（due / 满分 / status / score） |
| 成绩册 | `bb-cli grades [<课程>] [--due-only]` |
| 近期截止 | `bb-cli dues [--from D] [--to D] --format text` |
| 公告 | `bb-cli announcements [--course 子串] [--limit N]` |
| 课件清单 / 下载 | `bb-cli files <课程>` / `bb-cli fetch <课程> [-o 目录]` |
| 我的提交 | `bb-cli submission <课程> [--download]` |
| 身份 | `bb-cli whoami` |

课程参数接受课程 id（`_18027_1`）、课程代码或名称子串（`AIE3905`）；歧义时报候选清单。

## 状态值

`assignments` / `grades` 的 `status`：`Graded`=已评分（带 score）、`NeedsGrading`=已提交待评分、空/`None`=未提交或无数据。

## 时刻

`--format text` 的时间展示与 `--from` / `--to` / `--since` 过滤按本机时区；JSON 输出保持 API 原值（UTC ISO `…Z`）。

## 已知边界

- 学生会话 404：`gradebook/attempts`（平铺列表）、`discussion/forums`、`users/me/memberships`、`tasks`、`gradebook/grades`
- 仅 Classic（JSP）课程；Ultra 未验证
- 写操作（提交 / 发公告）刻意不提供
- 详表以 `connectors/bb-cli/README.md` 为唯一准源

## Prohibitions

- 绝不执行写操作（交作业 / 发公告等）；如需须用户明示并另行设计
- 学号 / 密码不入仓库、不回显密码；凭据只在 `~/.bb-cli/`

## Language

转述中文为主；课程名、课程代码、路径保留原形。
