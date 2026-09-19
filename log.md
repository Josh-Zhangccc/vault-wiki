# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-19）

工程定位：**个人自用**——矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：概念双插件 wiki/vault（纯声明）+ 桥接 mapping / lark-calendar（vault↔wiki、lark→calendar）+ 结构插件与 calendar 时间领地 + 外部指针族 lark（基座，指针/档案两形 + trust 懒刷新）、lark-docs（云文档域）、lark-im（人际域），共十九、无分层（注入序=依赖拓扑+字母序）；七命令 map/save/query/check/plugin/lark-map/wiki_plugin_kernel（末者为插件内核使用参考）。三投影一源：manifest（inject/checks/usage）→ AGENTS 注入区、check 检查块、命令用法块（consumes 序即执行序）；PLUGIN.md 纯文档，内核 wiki_plugin_kernel.py 唯一投影机；registry 字段注册表（预留段可认领回填）。docs/ 现行四件（quickstart/pointers/research×2）。`test-repo/` 自足虚拟库，根侧同步重拷。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）。原阶段③④⑤⑥（蒸馏/普世化/回填/自进化）不排期：模式重复时再蒸馏，回填随部署自然发生，自进化以「摩擦点即规范空洞」轻量随行。

## 下一步

- wiki 初始化机制（画像首建与建构/整合命令同批）：冷启动时机与首建内容——随设计文档一并解决
- lark 域扩展（im / calendar）与机械刷新（轮询 daemon、事件流）随真实使用再议
- 设计文档：导论随后开卷（章=文件，问题驱动；OKF 不收编）
- 部署进个人库（**用户自行执行**，agent 不主动触碰；走查见 `docs/quickstart.md`，additive，存量页不动、旧页渐进代理）
- skill 打磨随摩擦滚动；delegate（vault 放入通道）与裁撤项不排期

## 过往操作

- 2026-09-19 calendar 0.1 + lark-calendar 0.1：时间领地独立（月页两节制、冻结制、源开放），lark 为源适配器（桥接拓扑同 mapping）；日更 = cron 无人值守会话；link 0.10/0.11 孤儿判定路径制→type 制→对齐领地值集
- 2026-09-19 lark 0.2 档案页两形分区 + lark-im 0.1 人际域（群档/人档两分、涌现制入枢纽、关键人制、议题按需沉淀）
- 2026-09-19 index 0.10 溢出减负制：索引清单 ≤25 条，超窗按子树页数降序切出子目录自立索引；根恒在、纯函数重建、索引不发明结构；小库坍缩单索引（两库实测+合成用例实锤切出泄漏即修）
- 2026-09-19 lark 族立设（第十五/十六）：基座 0.1——`wiki/lark/<profile>/` 一企业一目录，指针页 token 身份证明 + trust 懒刷新，命令 lark-map；lark-docs 0.1——docs.md 枢纽三件套，全量映射禁；registry 扩 type lark；link 0.10 孤儿判定改 type 制；test-repo demo 冒烟
- 2026-09-16 市场调研入档 `docs/research-landscape.md`：同类入库/出库对标，Google OKF 谱系证实
- 2026-09-14 治理批次：structure 立设并 0.2（声明页 `wiki/structure.md` 块映射 + 漂移附检 diff）；vault 0.4 认领 url、mapping 0.7 孤儿报文带引用计数；todo 立设（第十三）；notes 0.13 type 分层；`docs/pointers.md` 指针概念成文；wikilib 中文键解析修补
- 2026-09-13 收束日：user-profile 立设（第十二）与画像调研入档；save 首跑纠偏——热缓存短名断链即修，裁定**工程是开发框架非跑库**（wiki 数据区归零）；quickstart 开卷、上 GitHub、评审修补、test-repo 立设、三投影一源定形
- 2026-09-12 定位与重构：裁定个人自用、以用代验；架构重构四提交；OKF v0.2 成文；SASU-L 与零污染纪律确立
- 2026-09-08~11 原型落地：六插件四命令起步；registry/actions 与装卸内核；命令-插件绑定、trust 立设
- 2026-09-07 插件规范草案写入 user-write（已删，见 git）
- 2026-08-26~28 创始期：个人库结构副本起建，旋即重定位为 vault-wiki 框架；一次骨架定稿经用户回退
