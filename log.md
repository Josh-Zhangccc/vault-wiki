# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-12）

工程处于原型验证期（阶段②），两轮真实操作完成（虚构库与真实库迁移各全过）。三库测试集矩阵定稿（人写金样/虚构剪藏/生成器交叉验证）。架构：九插件三层（origin：vault/notes/sessions；field：tag/link/trust；derived：index/hot/log）+ 五命令（owner×commands 绑定）+ 协议工件 + 双脚本（plugin_cli + pipeline 自证管道）。OKF v0.2 已对齐；提交纪律入 actions.md；附检覆盖 6/9；check 注入块机械化。规范 doc 后置；user-write/ 手稿只读。实验佐证入准则 9（ASRL 范式成文）。

## 阶段

① 架构与原型（✓）→ ② 真实操作验证（ingest/check 首轮，暴露盲点并修）→ ③ 规范蒸馏（从原型回写 docs）→ ④ 普世化（新实例复制）→ ⑤ 个人库回填（须用户指令）→ ⑥ 自进化（agent 自主析因优化，远景；地基=测试集）。当前：②。

## 下一步

- 建测试集矩阵：S 金样（质量面）、M 剪藏（离散面）、L 生成器（规模面）+ 缺陷注入与标注；随后全矩阵零污染基线校准
- P0 文档修补（样例化、指针机械校验）经矩阵对照验证后投入
- 实验余项：孤儿信噪比、hot dry-run、.gitignore、AGENTS.md 实例化手册
- 通用性漏点（阶段③④）：TYPE_ORDER 下放；AGENTS.md 双身分离

## 过往操作

- 2026-09-12 两轮实验：①虚构库「雾港」四命令全过；②真实库迁移——25 件只读复制入仓库外沙盒（拷 .meta + 12 行 AGENTS.md 一次立起，普世化前测过），10 个互不相通冷 session 时序摄入全过（全绿、零积压），词表 30 词、检索 3 组全中；实证并修复词表碎片化（wikilib 空白）与 query 提交指针缺口；归因会商确立 ASRL 实验范式与零提示污染纪律（准则 9）；测试集定稿三库矩阵交叉验证与人写金样，自进化列阶段⑥

- 2026-09-11 架构收尾（用户裁定均可执行）：命令-插件绑定显式化（owner×commands 双向声明，save=notes+sessions 双主，plugin_cli 校验无主/孤儿/单边）；trust 插件立设（field 层，认领 registry 预留信任四字段，层级推导不落盘）；机械项收编附检（link 断链/孤儿/别名二义、tag 层级深度、log 日期契约，附检覆盖 6/9）+ check 注入块机械化（自 PLUGIN.md 检查节投影）；提交纪律入 actions.md（数据区一次写一提交、verify 过才提交、agent 只 add 自写路径）。随行：手稿入库、smoke-tmp 清理、不立 git 插件

- 2026-09-10 两次落地：sessions 独立插件立设（领地 wiki/sessions/，participants=actor 列表留多 agent 位；notes 缩界，save 会话段移交）；分层与 OKF 对齐（插件分 origin/field/derived 三层 + 依赖方向校验；registry 对齐 OKF v0.2；log 归档改轨 archive/月；index 每目录化渐进披露；pipeline.py 写后管道与写后自证；viz 冒烟通过）

- 2026-09-09 三次推进：地基落地（registry/actions 协议工件、link 插件新立、命令锚点+预览前置、check 升级；依据个人库 128 页取证）；装卸机械化（plugin_cli 五命令幂等 + plugin 命令）；附检机制（audit 发现式执行 scripts/check.py，在场即注册）

- 2026-09-08 原型落地与对齐：原 wiki 思想转化为六插件 + 四命令（.meta/ 主本 + .agents/skills/ 副本 + AGENTS.md 注入区 + wiki 种子）；AGENTS.md 改写定「框架+原型」双定位与原型先行准则

- 2026-09-07 插件规范草案（manifest/依赖/生命周期/合规）应用户要求写入 user-write/2.md

- 2026-08-26~28 创始期：以个人库结构副本建立，旋即重定位为普世 vault-wiki 框架，AGENTS.md/log/docs 骨架就位；其间一次骨架定稿经用户决定回退
