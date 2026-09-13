# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-12）

工程定位裁定：**个人自用，尽快投入使用**——普世化与矩阵化测试裁撤，SASU-L 为镜，边用边改。2026-09-12 重构后架构：概念双插件 wiki/vault（纯声明）+ 桥接 mapping（原 vault 插件更名，领 map 命令）+ 八结构插件，共十一、无分层（注入序=依赖拓扑+字母序）；五命令 map/save/query/check/plugin；标识符英文化（触发词与 prose 留中文）。新形态待真实使用再验证（以用代验）。规范蒸馏开卷：OKF v0.2（`docs/01-okf.md`）。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）。原阶段③④⑤⑥（蒸馏/普世化/回填/自进化）不做排期：模式重复时再蒸馏，回填随部署自然发生，自进化以「摩擦点即规范空洞」的轻量形式随行。

## 下一步

- 设计文档重开卷：导论（目录 / USP / 设计理念 / 设计思路）先行，章 = 文件（受众 repo 读者，问题驱动式，OKF 不收编章节）
- 部署进个人库（**用户自行执行**，agent 不主动触碰：additive——拷 .meta + skills + AGENTS.md 注入 + wiki 骨架种子；存量页不动，新素材走命令，旧页渐进代理）
- skill 打磨随使用摩擦滚动，SASU-L 为镜；VAULT 治理（delegate 命令）后议
- 测试矩阵等裁撤项见 2026-09-12 裁定，不做排期

## 过往操作

- 2026-09-12 命令层收尾与文档对齐：ingest→map 更名瘦身（打磨询问移除，纯登记）；actions/registry/tag/check/README 随行（数据区提交模块词表英文化、log-archive 路径笔误修正）

- 2026-09-12 概念双插件立设：wiki/vault 各 v0.1（纯概念声明，无字段无命令；出身二分与只增条款分别移籍）；原 vault 插件更名 mapping v0.1（桥接件，depends vault+wiki，领命令 ingest）

- 2026-09-12 废分层：manifest 去 layer、plugin_cli 撤方向校验（保留存在性+无环）、注入序改依赖拓扑+字母序，两注入区重排；depends 语义放宽为「行为或语义依赖」

- 2026-09-12 标识符英文化：附检契约键 level/message、级别 info、TYPE_ORDER 六值（map/save/query/check/plugin/other）、hot 分节 Recent、PLUGIN/SKILL 节头、控制台输出；中文触发词与正文 prose 保留

- 2026-09-12 移除 user-write 手稿区：设计思路已吸取（agent 记忆理论、插件化草案），未执行设计不落库；引用点随行摘除（AGENTS/README/plugin 技能），全文存 git 历史

- 2026-09-12 README 重写为仓库门面：定位/它做什么/核心概念/布局/上手/指针，补人侧上手文档缺口

- 2026-09-12 投入使用前清理：移除雾港实验数据，数据区重置为空种子（hot/log 重置、index/tags 重建），verify 全绿零警告，AGENTS 指针随行

- 2026-09-12 OKF 成文：扫描确证从未落文字（仅 09-10 会商口径），蒸馏实现现状立 `docs/01-okf.md` 为权威定义（v0.2：三 MUST、保留名、渐进披露、署名与信任字段），registry/AGENTS 指针随行——反推问题闭合

- 2026-09-12 冷启动披露审计（check 全绿后行，零污染 subagent 通读全库）：A 层自动注入实证成立、主理解全中；猜点九条分诊——修补 trust/sessions 内联样例、actor 实例、OKF 外部规范标注、清遗留骨架；两账本边界与孤儿实况系 subagent 漏读非空洞

- 2026-09-12 定位裁定（用户）：个人自用、尽快投入使用——测试矩阵与交叉验证裁撤（experiments.md 改留 SASU-L 与零污染纪律），准则 9 改「披露完备、以用代验」，阶段表压缩，下一步转向个人库 additive 部署

- 2026-09-12 两轮实验：①虚构库「雾港」四命令全过；②真实库迁移——25 件只读复制入仓库外沙盒（拷 .meta + 12 行 AGENTS.md 一次立起，普世化前测过），10 个互不相通冷 session 时序摄入全过（全绿、零积压），词表 30 词、检索 3 组全中；实证并修复词表碎片化（wikilib 空白）与 query 提交指针缺口；归因会商确立 SASU-L 实验范式与零提示污染纪律（准则 9）；测试集定稿三库矩阵交叉验证与人写金样，自进化列阶段⑥

- 2026-09-11 架构收尾（用户裁定均可执行）：命令-插件绑定显式化（owner×commands 双向声明，save=notes+sessions 双主，plugin_cli 校验无主/孤儿/单边）；trust 插件立设（field 层，认领 registry 预留信任四字段，层级推导不落盘）；机械项收编附检（link 断链/孤儿/别名二义、tag 层级深度、log 日期契约，附检覆盖 6/9）+ check 注入块机械化（自 PLUGIN.md 检查节投影）；提交纪律入 actions.md（数据区一次写一提交、verify 过才提交、agent 只 add 自写路径）。随行：手稿入库、smoke-tmp 清理、不立 git 插件

- 2026-09-10 两次落地：sessions 独立插件立设（领地 wiki/sessions/，participants=actor 列表留多 agent 位；notes 缩界，save 会话段移交）；分层与 OKF 对齐（插件分 origin/field/derived 三层 + 依赖方向校验；registry 对齐 OKF v0.2；log 归档改轨 archive/月；index 每目录化渐进披露；pipeline.py 写后管道与写后自证；viz 冒烟通过）

- 2026-09-09 三次推进：地基落地（registry/actions 协议工件、link 插件新立、命令锚点+预览前置、check 升级；依据个人库 128 页取证）；装卸机械化（plugin_cli 五命令幂等 + plugin 命令）；附检机制（audit 发现式执行 scripts/check.py，在场即注册）

- 2026-09-08 原型落地与对齐：原 wiki 思想转化为六插件 + 四命令（.meta/ 主本 + .agents/skills/ 副本 + AGENTS.md 注入区 + wiki 种子）；AGENTS.md 改写定「框架+原型」双定位与原型先行准则

- 2026-09-07 插件规范草案（manifest/依赖/生命周期/合规）应用户要求写入 user-write/2.md

- 2026-08-26~28 创始期：以个人库结构副本建立，旋即重定位为普世 vault-wiki 框架，AGENTS.md/log/docs 骨架就位；其间一次骨架定稿经用户决定回退
