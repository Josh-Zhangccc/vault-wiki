# domain：域抽象（概念）

「外」的本体声明：wiki 只认内外，外侧由本插件定义——域（domain）是 wiki 外信息源的存在形态，即一份待填的适配器契约。本插件是概念声明：立抽象、定律与纪律，不拥有领地、字段、命令或脚本；具体域（vault / lark / project……）各自是插件，以 depends 边实例化。

## Structure

无自有结构与文件。实例化表达全在 depends 图：域本体插件直接依赖本插件，域内插件依赖各自域（structure → vault、lark-docs → lark），传递即成员；内侧插件（notes / sessions……）挂 wiki，不挂本插件。

## Invariants

契约六问（每域自答）：

- 外领地——信息住哪（`vault/`、lark-cli 可达系统、`projects/**`）
- 落地策略——借 vault 物化 / 自立容器 / 指针不落地
- 身份证明——vault：路径 + 哈希；lark：token↔页一比一；project：路径 + 声明页双向 diff
- wiki 侧属地——域投影页住哪（`wiki/vault/`、`wiki/lark/<profile>/`、声明页），属地路径由各域注入行自披露
- 写模型——只增 / 全权读写 / 可再生覆写
- 信任模型——原文不可变 / TTL 懒刷新 / 活文档

三定律：

- 落地选择本质是写模型选择：终态资产→只增仓储（vault）、过程容器→全权读写（project）、真相在别处→指针（lark）
- 翻译成本决定投影密度：任意格式→1:1 镜像、API 后→指针页、md 原生→仅声明披露
- 治理页在 wiki 内、治理对象在 wiki 外（structure.md 与 profile.md 同形）

两纪律：

- 借 vault 或指针为默认姿态，自立容器是例外——判据是写模型或结构刚性分叉（project 落 vault 即瘫痪是范例）
- 域须在 wiki 内可发现：声明页或注入行，未登记视为不存在

熵增落位：跨域语义消歧在 adapter 写入时完成、读时靠路径出身；wiki 内词表统一、链接图全连通；tag 教义不动（域内自由生长继续成立）。

## Changelog

- 0.1（2026-09-22）立设：蒸馏自 2026-09-19 域问题报告与四轮讨论；vault / lark / project 三实例先行合规
