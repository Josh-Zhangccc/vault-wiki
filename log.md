# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字；整合压缩须用户同意。

## 现状（2026-10-01）

工程定位：**个人自用**——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：双根概念 domain（外·域契约）/ wiki（内·出身二分）+ 域实例族 vault（默认域兼通用仓储，mapping 映射法则、structure 管布局）/ lark（外部域基座，域内 lark-docs/lark-im）/ project（自立容器域）/ email / bb（BB 课程域，bb-map 映射法则）+ calendar 时间领地（lark-calendar 源适配器）+ 横切件 notes/sessions/link/tag/trust/index/hot/log/user-profile/todo 与 tmp，共二十五插件、无分层（注入序=依赖拓扑+字母序）；八命令 map/save/profile/query/check/plugin/lark-map/wiki_plugin_kernel。三投影一源：manifest → AGENTS 注入区、check 检查块、命令用法块；内核 wiki_plugin_kernel.py 唯一投影机。docs/ 现行四件；test-repo/ 自足虚拟库（已同步二十五插件）。连接器 connectors/ 首件 bb-cli（CUHK-SZ Blackboard 只读 CLI，v0.1.3）。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）；模式重复再蒸馏，回填随部署发生。

## 下一步

- 日更 cron 与真实 profile 接入（部署侧）；email 连接器探路；bb-map 实验与命令化（组员）随后
- 设计文档：导论随后开卷（章=文件，问题驱动；OKF 不收编）
- 部署进个人库（用户自行执行；走查见 docs/quickstart.md，additive）
- skill 打磨随摩擦滚动；delegate 与裁撤项不排期

## 过往操作

- 2026-10-02 AGENTS 立临时迁移令 cleanup-sync：全员删旧文件、验旧史、重克隆并简报新规

- 2026-10-02 剔除资料整理Demo 整目录：真实课程样本 40MB 出库（历史留痕，见 10-01 行）

- 2026-10-02 bb 实验：四课 94 页、八问全中
- 2026-10-02 协作规范（实例页事故）：AGENTS 红线、准则 5 扩 README、README 转团队、test-repo 痕迹禁令

- 2026-10-01 bb v0.2 + bb-cli 0.1.4：公告分拣、inbox 即建、媒体分层、fetch 过滤与刷新；bb-map v0.7

- 2026-10-01 AGENTS 准则 6 行数上限拓宽至 250（注入区随插件增长）

- 2026-10-01 AGENTS 增准则 10 分析轮禁执行

- 2026-10-01 bb-map v0.4~0.6：桶名终裁（→courseware/assessments）；笔记节立而复撤（纯代理）；命令立设


- 2026-10-01 bb 域立设 v0.1（基石）；type 扩 bb
- 2026-10-01 bb-map v0.1→v0.3 立设并流，整合回 master
- 2026-10-01 bb-cli skill 移驻 connectors 并英文化

- 2026-10-01 summary 分支并入（资料整理Demo 后经历史清理）；框架零改动
- 2026-09-30 bb-cli 连修（v0.1.1~0.1.3）：UTC→本机时区；dues 双源合并（日历漏项成绩册兜底，AIE2001 实锤 4/5 缺）；announcements 单课失败降级（真凶=停用课程）；空结果提示、补 column_id；submission 命令封提交链路（列 attempt→文件→Classic download，REST download 404 绕行实证）
- 2026-09-29 bb-cli 立设 v0.1：ADFS 域前缀单步登录 + Learn REST 只读十五命令（curl_cffi 指纹），实测全通
- 2026-09-29 email 域与 profile 命令立设：email v0.1（账户+三资产+统一速写，全量禁/只读/发送明示）；user-profile 0.3 独立通道；domain/wiki/calendar 叙事补强；test-repo 重拷
- 2026-09-22~23 域化批次：domain 0.1 适配器契约（第二十二插件）；vault/wiki/lark/project/mapping/structure 对齐；老八件补 wiki 依赖边、注入序重排
- 2026-09-19 插件连发：lark 基座+docs/im；calendar+lark-calendar；project 0.2 容器外移；tmp 立设；index 溢出减负制；link 孤儿动态化
- 2026-09-14~16 治理与调研：structure/todo 立设、vault 0.4 认领 url、pointers 成文、市场调研入档
- 2026-09-13 收束日：user-profile 立设；裁定工程是开发框架非跑库（数据区归零）；quickstart/GitHub/test-repo/三投影定形
- 2026-09-12 定位重构：个人自用、以用代验；SASU-L 与零污染纪律确立
- 2026-09-08~11 原型落地：六插件四命令起步；registry/actions 与装卸内核；trust 立设
- 2026-08-26~28 创始期：个人库副本起建，旋即重定位为 vault-wiki 框架
