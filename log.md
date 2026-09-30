# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2.5k 字（2026-09-22 扩容）；整合压缩须用户同意。

## 现状（2026-09-29）

工程定位：**个人自用**——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：双根概念 domain（外·域契约）/ wiki（内·出身二分）+ 域实例族 vault（默认域兼通用仓储，mapping 映射法则、structure 管布局）/ lark（外部域基座，两形 + trust 懒刷新，域内 lark-docs/lark-im）/ project（自立容器域） / email + calendar 时间领地（lark-calendar 源适配器）、tmp、notes/sessions/link/tag/trust/index/hot/log/user-profile/todo，共二十三、无分层（注入序=依赖拓扑+字母序）；八命令 map/save/profile/query/check/plugin/lark-map/wiki_plugin_kernel（末者=内核参考）。三投影一源：manifest（inject/checks/usage）→ AGENTS 注入区、check 检查块、命令用法块（consumes 序即执行序）；PLUGIN.md 纯文档，内核 wiki_plugin_kernel.py 唯一投影机；registry 字段注册表（预留段可认领回填）。docs/ 现行四件（quickstart/pointers/research×2）。`test-repo/` 自足虚拟库，根侧同步重拷（域化后待重拷）。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）。原阶段③④⑤⑥不排期：模式重复再蒸馏，回填随部署发生，自进化轻量随行。

## 下一步

- bb-cli 待修（用户已知，缓办）：announcements 全扫遇单课公告工具关闭 400 即整体失败，待降级为跳过+报清单；log.md 已超 2.5k 上限，整合方案待用户点头
- 日更 cron 与真实 profile 接入（部署侧）；email 连接器探路；cuhksz_bb 域接 bb-cli 实验后立设
- 设计文档：导论随后开卷（章=文件，问题驱动；OKF 不收编）
- 部署进个人库（用户自行执行；走查见 `docs/quickstart.md`，additive）
- skill 打磨随摩擦滚动；delegate（vault 放入通道，structure 布局声明的消费者）与裁撤项不排期

## 过往操作

- 2026-09-30 bb-cli v0.1.1：截止时刻 UTC→本机时区（text 展示 + --from/--to/--since 过滤；JSON 保持 API 原值）——页面 23:59 与旧读数 15:59 差 8h 实锤
- 2026-09-29 bb-cli 连接器立设：`connectors/` 首件 v0.1——ADFS 域前缀（`cuhksz\学号`）单步登录 + Learn REST 只读十五命令（curl_cffi chrome124 指纹），实测全通；cuhksz_bb 域插件待实验
- 2026-09-29 email 域立设：v0.1，wiki/email/ 账户+三资产+统一速写，全量禁/只读/发送明示，无命令
- 2026-09-29 画像独立通道与叙事补强：profile 命令立设（user-profile 0.3 脱离 map/save 寄生、证据域放开 wiki 内页面、首建随触发自建、tag 明示不打；log 0.14 类型值集补 todo 漂移并扩 profile）；domain 补可对账域判据、wiki 0.6 出身三层与纪要说、calendar 借住记名；两裁定——depends 引用边保留不裁（存量自洽）、structure 维持 vault 域内件（消费者 = delegate 暂缓）；test-repo 重拷补域化欠账
- 2026-09-23 域化漏收补边：内侧老八件补 wiki 依赖边并进位——domain 0.1 挂 wiki 声明与 depends 图对齐；注入序重排（老八件降层、lark 族与 user-profile 顺延），kernel 全套投影同步
- 2026-09-22 域化批次（9.19 域报告四轮讨论收敛，domain 中心思想）：domain 0.1 立设（第二十二插件，适配器契约）；vault 0.5 默认域、wiki 0.5 属地泛化、lark/project 0.3 与 mapping 0.8 / structure 0.3 对齐、宪法叙事对齐——零机制变更，全声明级

- 2026-09-19 插件连发：lark 0.2 两形分区 + lark-im 0.1 人际域（群档人档、涌现、按需议题）；calendar 0.1 + lark-calendar 0.1（时间领地：月页两节制，lark 源适配器，日更=cron）；project 0.1→0.2 项目容器（工作区 projects/ + wiki 声明页双向 diff，本体出 wiki）；tmp 0.1 临时区（路径领地、隐身、断链豁免；index 0.11/link 0.13 配套）；link 0.10~0.13 孤儿判定动态化
- 2026-09-19 index 0.10 溢出减负制：清单 ≤25 条，超窗按子树页数降序切子目录自立索引；根恒在、纯函数、不发明结构；小库坍缩单索引（合成用例实锤）
- 2026-09-19 lark 族立设：基座 0.1（wiki/lark/<profile>/ 一企业一目录、token 证明、懒刷新）+ lark-docs 0.1（枢纽三件套、全量映射禁）
- 2026-09-16 市场调研入档 `docs/research-landscape.md`：同类入库/出库对标，Google OKF 谱系证实
- 2026-09-14 治理批次：structure 立设并 0.2（声明页 `wiki/structure.md` 块映射 + 漂移附检 diff）；vault 0.4 认领 url、mapping 0.7 孤儿报文带引用计数；todo 立设（第十三）；notes 0.13 type 分层；`docs/pointers.md` 指针概念成文；wikilib 中文键解析修补
- 2026-09-13 收束日：user-profile 立设（第十二）与画像调研入档；save 首跑纠偏——热缓存短名断链即修，裁定**工程是开发框架非跑库**（wiki 数据区归零）；quickstart 开卷、上 GitHub、评审修补、test-repo 立设、三投影一源定形
- 2026-09-12 定位与重构：裁定个人自用、以用代验；架构重构四提交；OKF v0.2 成文；SASU-L 与零污染纪律确立
- 2026-09-08~11 原型落地：六插件四命令起步；registry/actions 与装卸内核；命令-插件绑定、trust 立设
- 2026-09-07 插件规范草案写入 user-write（已删，见 git）
- 2026-08-26~28 创始期：个人库结构副本起建，旋即重定位为 vault-wiki 框架；一次骨架定稿经用户回退
