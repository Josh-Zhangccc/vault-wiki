# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意——团队态下整合权归负责人。

## 现状（2026-10-02）

工程定位：**团队项目**（2026-10-02 由个人自用转轨，协作红线见 AGENTS「用户要求」节）——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：双根概念 domain（外·域契约）/ wiki（内·出身二分）+ 域实例族 vault（默认域兼通用仓储，mapping 映射法则、structure 管布局）/ lark（外部域基座，域内 lark-docs/lark-im）/ project（自立容器域）/ email / bb（BB 课程域，bb-map 为映射法则 + 同名命令）+ calendar 时间领地（lark-calendar 源适配器）+ 横切件 notes/sessions/link/tag/trust/index/hot/log/user-profile/todo 与 tmp，共二十五插件、无分层（注入序=依赖拓扑+字母序）；九命令 map/save/profile/query/check/plugin/lark-map/bb-map/wiki_plugin_kernel。三投影一源：manifest → AGENTS 注入区、check 检查块、命令用法块，内核 wiki_plugin_kernel.py 唯一投影机。docs/ 现行四件；test-repo/ 独立测试沙箱（使用痕迹禁令）；connectors/ 首件 bb-cli v0.1.4。**两条临时令在挂：cleanup-sync、log-sync。**

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）；模式重复再蒸馏，回填随部署发生。

## 下一步

- 全员执行临时令并回执，负责人确认后移除；组员 bb-map v0.9 插件提交从干净分支重放（不带实例页）
- 修订指引落地：bb-cli 0.1.5（sanitize 保扩展名、媒体表、dues 过滤、目标路径参数）+ bb-map 规则批（计算列、共享要求文件、合集切分等，编号顺延）；AIE2040 补测提交件归位
- 笔记族 bb-notes 设计（挂缺）；日更 cron 与真实 profile 接入（部署侧）；email 连接器探路
- 设计文档：导论随后开卷（章=文件，问题驱动）；部署进个人库（走查见 docs/quickstart.md，additive）；skill 打磨随摩擦滚动

## 过往操作

- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 M1-M12 + term_status；v0.11 补录分节登记列不建页裁定

- 2026-10-02 指引清尾：C3 实为披露缺漏已补、todo v0.2 缺席即建、asset-read 立设（F1+F2）

- 2026-10-02 gh CLI 入管理者职责（GH_TOKEN 注入）

- 2026-10-02 bb v0.3：提醒双源、term_status、stale 粒度（D1~D3）

- 2026-10-02 迁移收口：临时令移除、备份与残枝清理

- 2026-10-02 管理者委托代行（审合推送治理，保留事项入册）；提交流程五步入宪法；dev 审合入库（bb-map v0.9 + bb-cli 0.1.5，C3 转指引）；PR 转推荐制

- 2026-10-02 bb 实验收官：四课落位 94 页、检索八问全中；实验报告与修订指引出（对话交付）
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队 + 痕迹禁令；Demo 40MB 出库并历史清理（特批）；临时令×2；log 治理（组员仅增）
- 2026-10-01 bb 域全套落地：bb 基石 v0.1→v0.2（公告分拣、inbox 缺席即建、媒体分层）；bb-map v0.1→v0.7（四桶终名 courseware/assessments，笔记节立而复撤，命令立设）；bb-cli v0.1.4（fetch 过滤与 --refresh）+ skill 移驻 connectors 并英文化；AGENTS 增准则 10（分析轮禁执行）、准则 6 拓至 250 行；summary 分支并入（demo 后经历史清理）
- 2026-09-29~30 连接器与域补设：bb-cli v0.1→0.1.3（ADFS 单步登录 + Learn REST 只读十五命令；UTC 本地化、dues 双源合并、submission 提交链路）；email 域 v0.1 与 profile 命令独立通道
- 2026-09-22~23 域化批次：domain 0.1 适配器契约；vault/wiki/lark/project/mapping/structure 对齐；老八件补 wiki 依赖边、注入序重排
- 2026-09-19 插件连发：lark 基座+docs/im；calendar+lark-calendar；project 0.2 容器外移；tmp 立设；index 溢出减负制；link 孤儿动态化
- 2026-09-14~16 治理与调研：structure/todo 立设、vault 0.4 认领 url、pointers 成文、市场调研入档
- 2026-09-13 收束日：user-profile 立设；裁定工程是开发框架非跑库；quickstart/GitHub/test-repo/三投影定形
- 2026-09-12 定位重构：以用代验；SASU-L 与零污染纪律确立
- 2026-09-08~11 原型落地：六插件四命令起步；registry/actions 与装卸内核；trust 立设
- 2026-08-26~28 创始期：个人库副本起建，旋即重定位为 vault-wiki 框架
