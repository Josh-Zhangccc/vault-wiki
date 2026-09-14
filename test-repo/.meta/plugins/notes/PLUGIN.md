# notes：原生笔记

出身就在 wiki 的知识——「原文」即 wiki 自身，vault 中无对应物。知识形态不作架构枚举（细分靠 type 字段，默认词表见 registry，实例开放自扩）。会话骨干页不在本区——归 sessions 插件；画像页归 user-profile。

## Structure

- `wiki/notes/**`，文件名自由（人起名，与镜像区的机械命名相对）
- 细分靠 type 字段，不靠目录——形态值开放（默认词表见 registry，实例自扩）；领地值 session / profile 封闭，必落各自领地

## Invariants

- 不可再生区：管道与命令不得覆盖重写既有笔记，只能新增或人手改
- 与 vault 代理层的边界由路径证明：wiki/vault/ 必有对应物，wiki/notes/ 必无
- 与 sessions / user-profile 的边界由 type 证明：type: session 落 `wiki/sessions/`、type: profile 落 `wiki/profile.md`，均不落本区

## Changelog

- 0.13（2026-09-14）瘦身（裁定：架构不承担形态分类职责）：正文与注入行去形态枚举——「概念/问答/决策/实体」为个人库实证迁移残留，且与 registry 漂移（漏 comparison）；type 分层：领地值封闭（source/session/profile，机械检查依据），形态值降实例默认词表（registry defaults，开放自扩）
- 0.12（2026-09-13）usage 更新语义缝合：更新 = 用户指令追加式并入（留痕）或人手改（专家评审：与 save 去重节两说）
- 0.11（2026-09-13）usage 去 type 枚举，值集唯一源 registry（消三重复述）
- 0.10（2026-09-13）注入源移交 manifest：删 Checks / Usage / Inject / Attachments 节，md 回归纯文档
- 0.9（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.8（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.7（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.6（2026-09-11）manifest 增 commands: [save]（save 由本插件与 sessions 共同驱动）
- 0.5（2026-09-10）缩界：会话骨干页移交 sessions 插件（独立领地 `wiki/sessions/`），本区留概念/问答/决策/实体
- 0.4（2026-09-10）type 枚举表述修正：以 registry 值集为准（消与注册表封闭性的矛盾）
- 0.3（2026-09-10）manifest 增 layer: origin（分层立设：出身层，零依赖）
- 0.2（2026-09-09）孤儿检查移交 link 插件（图性质归链接层）
- 0.1（2026-09-08）自原 wiki concepts/questions/comparisons/sessions 诸区合并简化（细分第二批）
