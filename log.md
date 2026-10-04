# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意——团队态下整合权归负责人。

## 现状（2026-10-04）

工程定位：**团队项目**（2026-10-02 转轨；红线与审合制见 AGENTS）——边用边改。架构终态：双根 domain（域契约）/ wiki（出身二分）+ 域实例族 vault / lark / project / email / bb（map·track·teach·quiz 四件族：track 管档案、teach/quiz 采集，素材落 notes/、提炼归 wiki）+ calendar + 横切件与 tmp，共二十八插件、无分层（拓扑+字母序；桥法则准则 11）；十三命令（见 README）。三投影一源（机制总纲见内核参考 skill）。docs/ 四件；test-repo/ 白名单镜像；connectors/ 首件 bb-cli v0.1.5。

## 阶段

框架构建（✓ 09-08~12）→ 日常使用与边用边改（**当前**）；模式重复再蒸馏，回填随部署。

## 下一步

- teach/quiz 首轮实测（伸缩、不越界、判分闭环）
- AIE2040 归位补测 + 复问失败问题
- bb-cli 用户信息优化；email 探路；日更 cron（部署侧）
- 设计文档导论开卷；部署进个人库；skill 打磨随摩擦

## 过往操作

- 2026-10-04 机制文档开卷：内核参考 skill v2——机制总述（形态/依赖/投影/绑定/桥法则/分层 + bb 示例），部署侧权威住所；PLUGIN.md 批次随后
- 2026-10-04 teach/quiz 改造（所有者裁定）：exams/ 废——素材归 bb notes/（ai 笔记平铺、考卷 testing/）、提炼归 wiki（判分回流 user.md）；bb-exam 更名 bb-quiz；bb-track v0.3 + 命令立设（用法挂载）；bb v0.7 notes/ 共居；teach v0.2 stale/冷启动
- 2026-10-04 治理：组员账号 CaoSuan-CODE 未经 PR 直推 master（bb-teach/bb-exam 立设 + test-repo 整体出跟踪，署名冒用所有者）——插件内容补审通过保留；所有者裁定 test-repo 白名单追踪回正；master 开分支保护（require PR、禁 force push）；通报归所有者
- 2026-10-04 bb-exam 立设：bb-track 的 testing 消费侧（插件 + 命令 + exams/ 容器）——指定范围+样例出英文题 + 中文解析，题型/难度对齐样例、不越界、解析回链 sm-N；插件 28、命令 12
- 2026-10-04 bb-teach 立设：bb-track 教学消费侧（插件 + 命令同名）——提问即讲解，二维伸缩（熟练度×难度）+ 术语门槛动态化 + 三层反馈闭环（单轮反馈不落盘、仅显著信号经确认收敛 user.md）；插件 27、命令 11
- 2026-10-02 全局域立宪三批（组会衍生）：准则 11 全局件/域件与桥；批一 kernel 必依校验 + log v0.15 域标 + 五基座补边；批二 todo/calendar/notes 派生归宿桥；批三 user-profile v0.4 认知桥 + bb-track 注册，mapping 边裁撤
- 2026-10-02 bb 认知线：bb v0.4 笔记区 + bb-track 立设（user.md 两区制、锚 sm-N）携 wiki v0.7 两形、bb-map 0.12 豁免；挂缺：课表源与课后触发
- 2026-10-02 组会（第 3 周）：笔记裁定→bb-track 方向；产品线头脑风暴（teach/test 已立，addition_check/bridge 待议）
- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 + v0.11 分节登记裁定补录
- 2026-10-02 修订指引五批全清（C/D/F/todo/M）；bb v0.3（D1~D3）；实验收官：四课 94 页、八问全中
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队；Demo 历史清理（特批）；临时令×2（毕撤）；管理者委托代行；dev 审合（bb-map v0.9 + bb-cli 0.1.5）
- 2026-10-01 bb 域全套落地：bb v0.1→0.2（公告分拣、inbox、媒体分层）；bb-map v0.1→0.7（四桶、命令）；bb-cli v0.1.4、skill 移驻 connectors；AGENTS 准则 10 与 250 行；summary 并入
- 2026-09-14~30 扩域与连发（细则见 git 史）：structure/todo 立设、pointers 与市场调研；lark 族（基座+docs/im）、calendar/lark-calendar、project 容器外移、tmp、index 溢出减负、link 孤儿动态化；domain 0.1 契约与五域对齐、老八件补边；bb-cli v0.1→0.1.3（ADFS+REST 只读、dues 双源）与 email 域、profile 命令
- 2026-08-26~09-13 个人期奠基（细则见 git 史）：创始副本起建旋即重定位 vault-wiki → 原型落地（六插件四命令、registry/actions、装卸内核、trust）→ 定位重构（以用代验、SASU-L、零污染）→ 收束定形（user-profile、「开发框架非跑库」裁定、quickstart/三投影）

> 2026-10-04 两度整合（负责人同意）；流水见 git 史。
