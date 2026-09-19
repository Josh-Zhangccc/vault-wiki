# lark：外部指针基座

wiki 的代理对象自本地 vault 外推到 CLI 可达的外部系统：以 lark-cli 为事实接口，立「指针页」——token 即身份证明（对照 mapping 代理页的路径 + 哈希证明），新鲜度交给 trust 层（stale 驱动 agent 现拉刷新，机械同步后置）。基座只立 profile 抽象与领地纪律，不载域知识：基座说「一企业一 profile，住在 wiki/lark/<profile>/」，域插件（lark-docs 等）收到后在每个 profile 下平行展开各自文件。

## Structure

- `wiki/lark/<profile>/`——一企业一目录，目录名 = `lark-cli --profile` 名（机械对应，agent 调用必带）
- `<profile>/profile.md`（kind: profile）——身份页：一句话、启用域说明（域枢纽页在场即启用）、TTL 覆写
- 新 profile = 建目录 + 身份页，全体现役域插件自动覆盖；领地披露走 index 派生链（渐进披露，wiki 根零新增特殊页）

## Invariants

- 指针页 `type: lark` + `lark` 块映射（profile / kind / token / url）；token↔页一比一，token 是身份证明，重命名靠 title + token 匹配
- trust 天花板 machine-confirmed：`stale_after` = 拉取日 + TTL（默认 7 天，身份页可覆写）；用前查 stale，stale 即带 `--profile` 现拉刷新——agent 即同步器
- 资源消失 → `status: deprecated`，不删
- 领地页面两形（0.2 起）：**指针页**全可再生——frontmatter 机械字段可覆写，珍贵内容蒸馏进 notes，不留在指针页；**档案页**分区制——frontmatter 机械区由对账维护，正文沉淀区只增不改（同 notes 待遇）；页面形态归域插件规范
- CLI 纪律：`--profile` 必带；auth 状态现查不落盘；入新域前 `lark-cli skills read <域>` 先行
- 命名小写 ASCII（目录与页面）

## Changelog

- 0.2（2026-09-19）立档案页两形分区制（frontmatter 机械区 / 正文沉淀区只增）——im 域档案页的架构前提；指针页语义不变
- 0.1（2026-09-19）立设：四轮设计收敛——指针-only 弃 vault 存储、profile 优先分段、trust 懒刷新代 daemon、基座/域插件分族（基座拥抽象，域插件平行服务）
