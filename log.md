# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-11）

工程处于原型验证期（阶段②）。架构：九结构插件分三层（origin：vault/notes/sessions；field：tag/link/trust；derived：index/hot/log，依赖方向由 plugin_cli 校验）+ 五命令（owner×commands 双向绑定：vault→ingest、notes/sessions→save，check/query/plugin=framework）+ 协议工件 + 双脚本（plugin_cli 生命周期；pipeline 写后管道 index/tags/hot/log/verify）。已对齐 OKF v0.2（status 三值、信任字段已由 trust 认领、actor 约定、渐进披露索引、归档改轨）；写后自证与提交纪律入 actions.md。附检覆盖 6/9 插件，check 注入块由 plugin_cli 自 PLUGIN.md 检查节机械化投影。规范 doc 后置；user-write/ 为用户手稿（agent 只读）。

## 阶段

① 架构与原型（✓）→ ② 真实操作验证（ingest/check 首轮，暴露盲点并修）→ ③ 规范蒸馏（从原型回写 docs）→ ④ 普世化（新实例复制）→ ⑤ 个人库回填（须用户指令）。当前：②（地基已就绪待验证）。

## 下一步

- 往 vault/ 放入首批资产，跑 ingest 全链路 + check 首审（重点验证：写后管道与 verify 自证、锚点读取、预览前置、提交纪律）
- 观察项：词表复用率、检索 log 行、stub 老化告警、verify 误报率；notes type→frontmatter 模板等首轮 save 漏写率实证；sessions 形状随首轮真实 save 校准

## 过往操作

- 2026-09-11 架构收尾（用户裁定均可执行）：命令-插件绑定显式化（owner×commands 双向声明，save=notes+sessions 双主，plugin_cli 校验无主/孤儿/单边）；trust 插件立设（field 层，认领 registry 预留信任四字段，层级推导不落盘）；机械项收编附检（link 断链/孤儿/别名二义、tag 层级深度、log 日期契约，附检覆盖 6/9）+ check 注入块机械化（自 PLUGIN.md 检查节投影）；提交纪律入 actions.md（数据区一次写一提交、verify 过才提交、agent 只 add 自写路径）。随行：user-write 手稿隐私核查后入库、smoke-tmp 清理并 gitignore、裁决不立 git 插件（过程层非结构）

- 2026-09-10 两次落地：sessions 独立插件立设（领地 wiki/sessions/，participants=actor 列表留多 agent 位；notes 缩界，save 会话段移交）；分层与 OKF 对齐（插件分 origin/field/derived 三层 + 依赖方向校验；registry 对齐 OKF v0.2；log 归档改轨 archive/月；index 每目录化渐进披露；pipeline.py 写后管道与写后自证；viz 冒烟通过）

- 2026-09-09 三次推进：地基落地（registry/actions 协议工件、link 插件新立、命令锚点+预览前置、check 升级；依据个人库 128 页取证）；装卸机械化（plugin_cli 五命令幂等 + plugin 命令）；附检机制（audit 发现式执行 scripts/check.py，在场即注册）

- 2026-09-08 原型落地与对齐：原 wiki 思想转化为六插件 + 四命令（.meta/ 主本 + .agents/skills/ 副本 + AGENTS.md 注入区 + wiki 种子）；AGENTS.md 改写定「框架+原型」双定位与原型先行准则

- 2026-09-07 插件规范草案（manifest/依赖/生命周期/合规）应用户要求写入 user-write/2.md

- 2026-08-26~28 创始期：以个人库结构副本建立，旋即重定位为普世 vault-wiki 框架，AGENTS.md/log/docs 骨架就位；其间一次骨架定稿经用户决定回退
