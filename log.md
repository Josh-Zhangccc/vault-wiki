# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-12）

工程定位裁定：**个人自用，尽快投入使用**——普世化与矩阵化测试裁撤，SASU-L 披露纪律保留为 skill 写作之镜，演进方式 = 边用边改。架构冻结为已验证现状：九插件三层（origin：vault/notes/sessions；field：tag/link/trust；derived：index/hot/log）+ 五命令（owner×commands 绑定）+ 协议工件 + 双脚本（plugin_cli + pipeline 自证管道，附检覆盖 6/9）。两轮真实操作已过（虚构库与真实库迁移各全过），不再追加预使用验证。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）。原阶段③④⑤⑥（蒸馏/普世化/回填/自进化）不做排期：模式重复时再蒸馏，回填随部署自然发生，自进化以「摩擦点即规范空洞」的轻量形式随行。

## 下一步

- 部署进个人库（**用户自行执行**，agent 不主动触碰：additive——拷 .meta + skills + AGENTS.md 注入 + wiki 骨架种子；存量页不动，新素材走命令，旧页渐进代理）
- skill 打磨随使用摩擦滚动，SASU-L 为镜
- 测试矩阵等裁撤项见 2026-09-12 裁定，不做排期

## 过往操作

- 2026-09-12 冷启动披露审计（check 全绿后行，零污染 subagent 通读全库）：A 层自动注入实证成立、主理解全中；猜点九条分诊——修补 trust/sessions 内联样例、actor 实例、OKF 外部规范标注、清遗留骨架；两账本边界与孤儿实况系 subagent 漏读非空洞

- 2026-09-12 定位裁定（用户）：个人自用、尽快投入使用——测试矩阵与交叉验证裁撤（experiments.md 改留 SASU-L 与零污染纪律），准则 9 改「披露完备、以用代验」，阶段表压缩，下一步转向个人库 additive 部署

- 2026-09-12 两轮实验：①虚构库「雾港」四命令全过；②真实库迁移——25 件只读复制入仓库外沙盒（拷 .meta + 12 行 AGENTS.md 一次立起，普世化前测过），10 个互不相通冷 session 时序摄入全过（全绿、零积压），词表 30 词、检索 3 组全中；实证并修复词表碎片化（wikilib 空白）与 query 提交指针缺口；归因会商确立 SASU-L 实验范式与零提示污染纪律（准则 9）；测试集定稿三库矩阵交叉验证与人写金样，自进化列阶段⑥

- 2026-09-11 架构收尾（用户裁定均可执行）：命令-插件绑定显式化（owner×commands 双向声明，save=notes+sessions 双主，plugin_cli 校验无主/孤儿/单边）；trust 插件立设（field 层，认领 registry 预留信任四字段，层级推导不落盘）；机械项收编附检（link 断链/孤儿/别名二义、tag 层级深度、log 日期契约，附检覆盖 6/9）+ check 注入块机械化（自 PLUGIN.md 检查节投影）；提交纪律入 actions.md（数据区一次写一提交、verify 过才提交、agent 只 add 自写路径）。随行：手稿入库、smoke-tmp 清理、不立 git 插件

- 2026-09-10 两次落地：sessions 独立插件立设（领地 wiki/sessions/，participants=actor 列表留多 agent 位；notes 缩界，save 会话段移交）；分层与 OKF 对齐（插件分 origin/field/derived 三层 + 依赖方向校验；registry 对齐 OKF v0.2；log 归档改轨 archive/月；index 每目录化渐进披露；pipeline.py 写后管道与写后自证；viz 冒烟通过）

- 2026-09-09 三次推进：地基落地（registry/actions 协议工件、link 插件新立、命令锚点+预览前置、check 升级；依据个人库 128 页取证）；装卸机械化（plugin_cli 五命令幂等 + plugin 命令）；附检机制（audit 发现式执行 scripts/check.py，在场即注册）

- 2026-09-08 原型落地与对齐：原 wiki 思想转化为六插件 + 四命令（.meta/ 主本 + .agents/skills/ 副本 + AGENTS.md 注入区 + wiki 种子）；AGENTS.md 改写定「框架+原型」双定位与原型先行准则

- 2026-09-07 插件规范草案（manifest/依赖/生命周期/合规）应用户要求写入 user-write/2.md

- 2026-08-26~28 创始期：以个人库结构副本建立，旋即重定位为普世 vault-wiki 框架，AGENTS.md/log/docs 骨架就位；其间一次骨架定稿经用户决定回退
