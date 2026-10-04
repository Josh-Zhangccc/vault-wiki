# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意——团队态下整合权归负责人。

## 现状（2026-10-04）

工程定位：**团队项目**（2026-10-02 转轨；协作红线见 AGENTS「用户要求」节；master 已开分支保护——PR 审合制，直推被机制拒绝）——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：双根概念 domain / wiki（出身二分，属地两形：代理页 + 域内原生页）+ 域实例族 vault（默认域兼通用仓储，mapping 映射法则、structure 管布局）/ lark（外部域基座，域内 docs/im）/ project（自立容器域）/ email / bb（课程工作区 + 属地，bb-map 映射法则、bb-track 认知档案 + 消费侧 bb-teach 教学讲解 / bb-exam 出题自测，exams/ 容器）+ calendar 时间领地（lark-calendar 源适配器）+ 横切件 notes/sessions/link/tag/trust/index/hot/log/user-profile/todo 与 tmp，共二十八插件、无分层（注入序=依赖拓扑+字母序；全局件桥法则见准则 11）；十二命令 map/save/profile/query/check/plugin/lark-map/bb-map/asset-read/wiki_plugin_kernel/bb-teach/bb-exam。三投影一源：manifest → AGENTS 注入区、check 检查块、命令用法块，内核 wiki_plugin_kernel.py 唯一投影机。docs/ 现行四件；test-repo/ 沙箱白名单式追踪（仅 .meta/.agents 镜像）；connectors/ 首件 bb-cli v0.1.5。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）；模式重复再蒸馏，回填随部署发生。

## 下一步

- bb-teach / bb-exam 首轮真实使用验证（二维伸缩与不越界约束的实测量）
- 收尾验证：AIE2040 提交件归位补测 + 复问此前失败问题
- bb-cli 用户信息优化；email 探路；日更 cron（部署侧）
- 设计文档：导论开卷（章=文件，问题驱动）；部署进个人库（docs/quickstart.md，additive）；skill 打磨随摩擦滚动

## 过往操作

- 2026-10-04 治理：组员账号 CaoSuan-CODE 未经 PR 直推 master（bb-teach/bb-exam 立设 + test-repo 整体出跟踪，署名冒用所有者）——插件内容补审通过保留；所有者裁定 test-repo 白名单式追踪（仅 .meta/.agents 镜像入库）回正未授权变更；master 开分支保护（require PR、禁 force push）；组内通报由所有者发出
- 2026-10-04 bb-exam 立设：bb-track 的 testing 消费侧（插件 + 命令 + exams/ 容器）——指定范围+样例出英文题 + 中文解析，题型/难度对齐样例、不越界、解析回链 sm-N；插件 28、命令 12
- 2026-10-04 bb-teach 立设：bb-track 教学消费侧（插件 + 命令同名）——提问即讲解，二维伸缩（熟练度×难度）+ 术语门槛动态化 + 三层反馈闭环（单轮反馈不落盘、仅显著信号经确认收敛 user.md）；插件 27、命令 11
- 2026-10-02 全局域立宪三批（组会衍生）：准则 11 全局件/域件与桥；批一 kernel 必依校验 + log v0.15 域标 + 五基座补边（vault/project 原缺 trust）；批二 todo/calendar/notes 派生归宿桥；批三 user-profile v0.4 认知桥 + bb-track 注册，mapping 边裁撤（校验实测抓出误判）
- 2026-10-02 bb 认知线：bb v0.4 笔记区（外容器→课程工作区，notes/ 归人）+ bb-track 立设（user.md 两区制、锚 sm-N、应知不存、笔记三属性）携 wiki v0.7 属地两形、bb-map 0.12 豁免；挂缺：课表源（SIS/ics）与课后触发
- 2026-10-02 组会（第 3 周）：笔记裁定→bb-track 方向；产品线头脑风暴（teaching/testing/addition_check/bridge）；teach-test 归吴
- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 + v0.11 分节登记裁定补录
- 2026-10-02 修订指引五批全清（C/D/F/todo/M）；bb v0.3（D1~D3）；实验收官：四课 94 页、八问全中
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队；Demo 历史清理（特批）；临时令×2（毕撤）；管理者委托代行；dev 审合（bb-map v0.9 + bb-cli 0.1.5）
- 2026-10-01 bb 域全套落地：bb v0.1→0.2（公告分拣、inbox 即建、媒体分层）；bb-map v0.1→0.7（四桶终名、命令立设）；bb-cli v0.1.4、skill 移驻 connectors；AGENTS 准则 10 与 250 行；summary 分支并入
- 2026-09-14~30 扩域与连发（细则见 git 史）：structure/todo 立设、pointers 成文、市场调研入档；lark 族（基座+docs/im）+ calendar/lark-calendar + project 容器外移 + tmp 立设 + index 溢出减负 + link 孤儿动态化；domain 0.1 适配器契约与五域对齐、老八件补边与注入序重排；bb-cli v0.1→0.1.3（ADFS 登录+REST 只读、UTC 本地化、dues 双源）与 email 域、profile 命令
- 2026-08-26~09-13 个人期奠基（两轮，细则见 git 史）：创始副本起建旋即重定位 vault-wiki 框架 → 原型落地（六插件四命令、registry/actions、装卸内核、trust）→ 定位重构（以用代验、SASU-L、零污染纪律）→ 收束定形（user-profile、裁定「开发框架非跑库」、quickstart/GitHub/test-repo/三投影）

> 2026-10-04 经负责人同意整合压缩：现状刷新、9 月流水归并；完整流水见 git 提交史。
