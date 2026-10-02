# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意——团队态下整合权归负责人。

## 现状（2026-10-02）

工程定位：**团队项目**（2026-10-02 由个人自用转轨，协作红线见 AGENTS「用户要求」节）——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：双根概念 domain（外·域契约）/ wiki（内·出身二分，属地两形：代理页 + 域内原生页）+ 域实例族 vault（默认域兼通用仓储，mapping 映射法则、structure 管布局）/ lark（外部域基座，域内 lark-docs/lark-im）/ project（自立容器域）/ email / bb（BB 课程域：课程工作区，bb-map 为映射法则 + 同名命令，bb-track 管认知档案）+ calendar 时间领地（lark-calendar 源适配器）+ 横切件 notes/sessions/link/tag/trust/index/hot/log/user-profile/todo 与 tmp，共二十六插件、无分层（注入序=依赖拓扑+字母序）；十命令 map/save/profile/query/check/plugin/lark-map/bb-map/asset-read/wiki_plugin_kernel。三投影一源：manifest → AGENTS 注入区、check 检查块、命令用法块，内核 wiki_plugin_kernel.py 唯一投影机。docs/ 现行四件；test-repo/ 独立测试沙箱（使用痕迹禁令）；connectors/ 首件 bb-cli v0.1.5。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）；模式重复再蒸馏，回填随部署发生。

## 下一步

- 桥批次：user-profile v0.4 认知桥 + bb-track 注册行 + 全局件/域件法则一句入准则（方案已裁定）
- 收尾验证：AIE2040 提交件归位补测 + 复问此前失败问题
- bb-cli 用户信息优化；email 连接器探路；日更 cron 与真实 profile 接入（部署侧）
- 设计文档：导论开卷（章=文件，问题驱动）；部署进个人库（docs/quickstart.md，additive）；skill 打磨随摩擦滚动

## 过往操作

- 2026-10-02 bb-track v0.1 立设：认知档案 user.md 两区制（读数收敛+证据流只增、锚 sm-N、应知不存、学期边界）+ 笔记只读消费三属性；携 wiki v0.7 属地两形（域内原生页首例）、bb-map v0.12 豁免
- 2026-10-02 挂缺：课表源（SIS/ics，归 calendar 适配器）与课后时间触发——bb-track v0.1 非目标
- 2026-10-02 bb v0.4：笔记区立设（组会裁定）——外容器拉取物仓储→课程工作区，保留子区 notes/ 归人全权，机器写边界显式化
- 2026-10-02 组会（第 3 周）：笔记裁定→bb-track 方向；产品线头脑风暴（teaching/testing/addition_check/bridge）；teach-test 归吴
- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 + v0.11 分节登记裁定补录
- 2026-10-02 指引清尾（C/D/F/todo/M 五批全清）：C3 披露补、todo v0.2 缺席即建、asset-read 立设
- 2026-10-02 bb v0.3：提醒双源、term_status、stale 粒度（D1~D3）
- 2026-10-02 bb 实验收官：四课 94 页、检索八问全中；报告与修订指引出
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队；Demo 历史清理（特批）；临时令×2（毕撤）；管理者委托代行 + gh 入责 + dev 分支审合（bb-map v0.9 + bb-cli 0.1.5）
- 2026-10-01 bb 域全套落地：bb v0.1→0.2（公告分拣、inbox 即建、媒体分层）；bb-map v0.1→0.7（四桶终名、命令立设）；bb-cli v0.1.4、skill 移驻 connectors；AGENTS 准则 10 与 250 行；summary 分支并入
- 2026-09-29~30 连接器与域补设：bb-cli v0.1→0.1.3（ADFS 登录 + REST 只读；UTC 本地化、dues 双源、submission 链路）；email 域与 profile 命令
- 2026-09-22~23 域化批次：domain 0.1 适配器契约；vault/wiki/lark/project/mapping/structure 对齐；老八件补 wiki 依赖边、注入序重排
- 2026-09-19 插件连发：lark 基座+docs/im；calendar+lark-calendar；project 0.2 容器外移；tmp 立设；index 溢出减负制；link 孤儿动态化
- 2026-09-14~16 治理与调研：structure/todo 立设、vault 0.4 认领 url、pointers 成文、市场调研入档
- 2026-09-13 收束日：user-profile 立设；裁定工程是开发框架非跑库；quickstart/GitHub/test-repo/三投影定形
- 2026-09-12 定位重构：以用代验；SASU-L 与零污染纪律确立
- 2026-09-08~11 原型落地：六插件四命令起步；registry/actions 与装卸内核；trust 立设
- 2026-08-26~28 创始期：个人库副本起建，旋即重定位为 vault-wiki 框架
