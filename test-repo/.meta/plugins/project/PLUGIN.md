# project：项目容器

项目 = 有目标、有阶段、有完成判据的中长期事项，本体是**真实工作区**：根下第三容器 `projects/<项目名>/`，agent 全权读写（与 vault 的「只增」相对——工作区 vs 资产库）。wiki 端只做披露：声明页告诉 agent 有哪些项目、各是什么；跟踪信息住在项目文件夹内（项目自足：进目录即得全部上下文，本仓库自身即此形态的活例）。

## Structure

- `projects/<项目名>/`——项目工作区；结构自由（代码、文档、素材皆可），惯例带自述 `project.md`
- `project.md`（工作区自述，非 wiki 页）：frontmatter 从简（title / stage / due 可选；stage 词表：规划 / 进行 / 暂停 / 完成，开放）；正文四区沿用行级轻量——目标与上下文 / 阶段（编号+checkbox+目标日期）/ 任务（`- [ ] 一句话（截止 YYYY-MM-DD）`，行不建页）/ 决策（`- 日期 决定 X 因为 Y`，只增）
- `wiki/projects.md`（type: project）——声明页：frontmatter `projects` 块映射 = 项目名→一句话（机器可读）；正文放横切备注

## Invariants

- wiki 只披露不承载：项目内容不进 wiki（涉及项目内容的检索直查 `projects/` 子树）；声明页是唯一 wiki 侧产物
- 声明与现状双向 diff（structure 先例）：声明的项目无目录 → warning；目录未声明 → warning；处置属人
- 与 todo 边界不变：todo 是 agent 委托活工作集，`project.md` 任务是持久分解事实源
- 完成判据达成 → 自述 `stage: 完成`；工作区不删，声明页可注明
- 与 vault 边界：vault 存资产（命令侧只增），projects 存工作区（全权读写）——需要改动既有文件的工作进 projects，存放与产出物进 vault

## Changelog

- 0.2（2026-09-19）本体出 wiki：项目落根容器 `projects/<名>/`（工作区，agent 全权读写），四区自述随项目（`project.md`），wiki 端收敛为声明页 + 双向 diff（structure 先例第二消费者）；0.1 的 `wiki/projects/` 领地退役
- 0.1（2026-09-19）立设：一项目一页四区制、stage 开放词表、todo 边界、任务行轻量（先轻后重裁定）
