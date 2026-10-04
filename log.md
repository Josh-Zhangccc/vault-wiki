# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意——团队态下整合权归负责人。

## 现状（2026-10-04）

工程定位：**团队项目**（2026-10-02 转轨；红线与审合制见 AGENTS）——边用边改。架构终态：双根 domain / wiki + 域实例族 vault / lark / project / email / bb（map·track·teach·quiz 四件族，素材落 notes/ 提炼归 wiki）+ calendar + 横切件与 tmp，共三十插件、无分层（拓扑+字母序；桥法则准则 11）；十三命令（见 README）。三投影一源（机制总纲见内核参考 skill）。test-repo/ 白名单镜像；connectors/ 首件 bb-cli v0.1.5。

## 阶段

框架构建（✓ 09-08~12）→ 日常使用与边用边改（**当前**）。

## 下一步

- teach/quiz 首轮实测（伸缩/越界/判分）
- AIE2040 归位补测 + 复问失败问题
- bb-cli 用户信息优化；email 探路；日更 cron（部署侧）
- sis-cli v0.2：grades 组件 term 交互查询与结构化解析、周课表星期归属、学费/考试计划组件登记（raw 探路）

## 过往操作

- 2026-10-05 连接器：sis-cli v0.1 立设——SIS（PeopleSoft CS）只读 CLI：同源 ADFS OAuth2 复用、code 经 CUSZ_SSO_LOGIN 表单消费、PS_DEVICEFEATURES 破壳、psc+PTCNAV 组件直击；schedule 全解析（周事件+学期课程）、grades/center/history/appt 文本摘要、raw 透传；只读红线（选课类永不提供）；实证含组件 URL 双源（浏览器菜单+HTTP）
- 2026-10-04 部署收整：april-linux 实例库自 ~ 迁 ~/repo（库与上游原本分离——~/vault-wiki 为升级源，connectors 随迁）；家级 .agents 回归纯 lark skill，孤儿警告根治；dsh 升 0.2.0-rc.2 并修四插件适配
- 2026-10-04 部署：首座实例库落地 april-linux（家目录即库根）——机器清理三清单、clone 工程仓为升级源、三十插件收敛 verify 全绿、首批设备页两件（april-linux / windows-dev，互设 related）；device v0.2 增工具环境摘要节（在场级、多设备互查注册表、外壳以指针引页）先此入库
- 2026-10-04 插件：device v0.1 立设——设备档案复用 notes 领地（type: entity 建议、零 type 扩值），device 块映射最小键集（serial/purchased/warranty_until），附检临期扫描 30 天窗口、到期经确认受托入 todo；零命令零新领地
- 2026-10-04 插件：语言中性化清理批——tag v0.11（「中文为主」拆除，主语言跟 language 页 default 键）+ 八命令主本输出语言节统一改写（map/lark-map/profile/bb-map/bb-track/asset-read/query/save）；纪律级语言硬编码清零（余 AGENTS 准则 7 为开发期实例事实）；calendar 月页节名待裁
- 2026-10-04 插件：语言中性化批——language v0.2（缺席回落改跟会话语言，中文降为开发期实例事实；分层裁定：源对齐归域件、读者对齐归声明页键）+ bb-quiz v0.4（拆除「英文试题+中文解析」硬编码：题干源对齐、解析读者对齐 annotation 键）+ bb-teach v0.4（讲解语言取 teaching 键 + 术语锚点集优先全局表兜底）；国际生实例零改动可用
- 2026-10-04 插件：language v0.1 立设——行文声明页（language/terms 块映射 + 沉淀节两形分区），产出语言与行文基线、缺席容忍、默认基线非强制（域件特例优先）、术语涌现制；usage_routes 落 save（源侧路由首批应用）；test-repo 镜像重拷
- 2026-10-04 沙箱使用文档开卷 sandbox.md；沙箱重置并初始化外壳
- 2026-10-04 内核：cmd-inject 升源侧路由——manifest usage_routes 装即落投影、重复路由校验、披露序定序、ls 路由表；bb 族迁移（teach/quiz v0.3、track v0.4 命令瘦身）
- 2026-10-04 行文修订三批：docs 四件、README 与插件文档统一重写
- 2026-10-04 PLUGIN.md 二十八件分四批升格设计文档：设计概要节——为什么/族内位置/关键裁定与弃案/机制回指；六桥节按分工裁定降格；plugin 与内核参考 skill 形态规格对齐
- 2026-10-04 docs 补全：mechanics 机制详解（含域的生长节）与 usage 使用指南开卷，指针接线与陈旧修正，test-repo 镜像对齐
- 2026-10-04 docs 立卷：删 00/01/pointers，intro 导论与 quickstart v2 开卷，research×2 留，迁 .meta/docs，内核参考 skill v2 立机制总纲
- 2026-10-04 teach/quiz 改造（所有者裁定）：exams/ 废——素材归 bb notes/、提炼归 wiki（判分回流）；bb-exam 更名 bb-quiz；bb-track v0.3 + 命令；bb v0.7 共居
- 2026-10-04 治理：组员 CaoSuan-CODE 直推 master（署名冒用）——内容补审保留；test-repo 白名单追踪回正；master 开分支保护
- 2026-10-04 bb-teach/bb-exam 初版立设（组员）：teach 二维伸缩讲解 + 三层反馈；exam 范围出题 + 判分——后经所有者裁定改造（见上）
- 2026-10-02 全局域立宪三批（组会衍生）：准则 11 全局件/域件与桥；批一必依校验 + log 域标 + 基座补边；批二 todo/calendar/notes 派生归宿桥；批三认知桥 + bb-track 注册，mapping 边裁撤
- 2026-10-02 bb 认知线：bb v0.4 笔记区 + bb-track 立设（user.md 两区制、锚 sm-N）携 wiki v0.7、bb-map 0.12；挂缺：课表源与课后触发
- 2026-10-02 组会（第 3 周）：笔记裁定→bb-track 方向；产品线头脑风暴（teach/test 已立，addition_check/bridge 待议）
- 2026-10-02 PR #1 审合入库：bb-map v0.10 规则批 + v0.11 分节登记裁定补录
- 2026-10-02 修订指引五批全清（C/D/F/todo/M）；bb v0.3（D1~D3）；实验收官：四课 94 页、八问全中
- 2026-10-02 治理日：实例页事故→三红线 + README 转团队；Demo 历史清理（特批）；临时令×2（毕撤）；管理者委托代行；dev 审合（bb-map v0.9 + bb-cli 0.1.5）
- 2026-10-01 bb 域全套落地：bb v0.1→0.2（公告分拣、inbox、媒体分层）；bb-map v0.1→0.7（四桶、命令）；bb-cli v0.1.4、skill 移驻 connectors；AGENTS 准则 10 与 250 行；summary 并入
- 2026-09-14~30 扩域与连发（细则见 git 史）：structure/todo 立设、pointers 与市场调研；lark 族（基座+docs/im）、calendar/lark-calendar、project 容器外移、tmp、index 溢出减负、link 孤儿动态化；domain 0.1 契约与五域对齐、老八件补边；bb-cli v0.1→0.1.3（ADFS+REST 只读、dues 双源）与 email 域、profile 命令
- 2026-08-26~09-13 个人期奠基（细则见 git 史）：创始副本起建旋即重定位 vault-wiki → 原型落地（六插件四命令、registry/actions、装卸内核、trust）→ 定位重构（以用代验、SASU-L、零污染）→ 收束定形（user-profile、「开发框架非跑库」裁定、quickstart/三投影）

> 2026-10-04 多度整合（负责人同意）。
