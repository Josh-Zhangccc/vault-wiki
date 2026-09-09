# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-08）

工程转入原型驱动，仓库兼框架工程与原型实例。插件+命令架构落地：六结构插件（vault/log/hot/tag/index/notes）+ 四命令（check/ingest/save/query，lint 已并入 check），.meta/ 主本、.agents/skills/ 副本、AGENTS.md 注入区、wiki 种子就位（提交 98d9a73）。原个人库思想已全部转化（只读）；规范 doc 后置；user-write/ 为用户手稿（agent 只读）；工程正式名待定。

## 阶段

① 架构与原型（✓ 讨论收敛 + 落地）→ ② 真实操作验证（ingest/check 首轮，暴露盲点并修）→ ③ 规范蒸馏（从原型回写 docs）→ ④ 普世化（新实例复制）→ ⑤ 个人库回填（须用户指令）。当前：②。

## 下一步

- 往 vault/ 放入首批资产，跑 ingest 全链路 + check 首审
- 验证暴露的问题回修插件/命令与注入块
- 规范蒸馏（docs 后置回写）；README 随现状更新

## 过往操作

- 2026-09-08 对齐现状：AGENTS.md 改写（框架+原型双定位、原型先行准则、指针更新），log 阶段重写；docs/00 用户精简一并入库

- 2026-09-08 原型落地：原 wiki 思想转化为六结构插件（vault/log/hot/tag/index/notes）与四命令（check/ingest/save/query，lint 并入 check），.meta/ 主本 + .agents/skills/ 部署副本 + AGENTS.md 注入区 + wiki 种子就位；doc 后置，user-write 未动，个人库只读

- 2026-09-07 插件规范草案：协议讨论（manifest / scope / 依赖 / 生命周期 / 合规检查）应用户要求写入 user-write/2.md；先前误落的 .meta/plugins/test/ 实体已撤（自检脚本留存于提交 959f353）

- 2026-08-28 00 状态对齐：docs/00 frontmatter draft→final，闭合与 README「已定稿」、宪法上游定位的口径不一致

- 2026-08-28 撤销骨架定稿：应用户决定保留工作区回退（删 docs/01、log 同步回退）；AGENTS.md 指针、docs/00 §七、README 引用一并同步；旧版见提交 cb09895

- 2026-08-28 初始化：清空旧副本内容（保留 .git）；AGENTS.md、log.md、.gitignore、目录结构就位；三个骨架分叉经用户授权代裁（代理层双目录 sources+notes；raw 归档区子结构实例自定；hot 预留位默认开），写入 docs/01；首次提交
- 2026-08-28 重定位：工程由「个人库副本」转为「普世 vault-wiki 框架」；写入 README、docs/00-principles
- 2026-08-26 前身：作为个人库结构副本建立（沙箱用途）
