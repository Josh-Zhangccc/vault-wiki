# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-13）

工程定位：**个人自用，尽快投入使用**——普世化与矩阵测试裁撤，SASU-L 为镜，边用边改。架构终态：概念双插件 wiki/vault（纯声明）+ 桥接 mapping + 八结构插件，共十一、无分层（注入序=依赖拓扑+字母序）；六命令 map/save/query/check/plugin/wiki_plugin_kernel（末者为插件内核使用参考）。三投影一源：manifest（inject / checks / usage）→ AGENTS 注入区、check 检查块、命令用法块（consumes 有序声明，序即执行序）；PLUGIN.md 回归纯文档（Role / Structure / Invariants / Changelog），插件内核 wiki_plugin_kernel.py 为唯一投影机。格式契约内化插件（根索引自述 format_version），vault 大小写统一；docs/ 不起现行作用。新形态以用代验。

## 阶段

框架构建（✓，2026-09-08~12）→ 日常使用与边用边改（**当前**）。原阶段③④⑤⑥（蒸馏/普世化/回填/自进化）不排期：模式重复时再蒸馏，回填随部署自然发生，自进化以「摩擦点即规范空洞」轻量随行。

## 下一步

- 设计文档重开卷：导论（目录/USP/理念/思路）先行，章=文件（repo 读者、问题驱动；OKF 不收编）
- 部署进个人库（**用户自行执行**，agent 不主动触碰；additive：拷 .meta + skills + AGENTS 注入 + wiki 骨架种子，存量页不动、旧页渐进代理）
- skill 打磨随使用摩擦滚动；vault 治理（delegate）后议；测试矩阵等裁撤项不排期

## 过往操作

- 2026-09-13 投影体系定形（六提交）：概念双插件纯化；格式契约内化（okf_version→format_version、VAULT 统一小写）；第三投影立设（consumes 有序声明 + 命令注入区，命令瘦身去手抄）；注入源全归 manifest（PLUGIN.md 回归纯文档）；内核定名 wiki_plugin_kernel 并立同名参考命令

- 2026-09-12 定位与重构：裁定个人自用、以用代验（矩阵测试裁撤）；架构重构四提交（标识符英文化、废分层、概念双插件立设、ingest→map 更名）；OKF v0.2 成文 + 冷启动披露审计；雾港虚构库与真实库两轮实验全绿，确立 SASU-L 与零污染纪律；投入使用准备（清实验数据、README 门面化）

- 2026-09-08~11 原型落地与收尾：六插件四命令起步；registry/actions 协议工件与装卸内核；分层对齐（log 归档改轨、index 每目录化、pipeline 写后管道与自证）；命令-插件双向绑定、trust 立设、附检收编

- 2026-09-07 插件规范草案写入 user-write（已删，见 git）

- 2026-08-26~28 创始期：个人库结构副本起建，旋即重定位为 vault-wiki 框架；一次骨架定稿经用户回退
