# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-09）

工程处于原型验证期（阶段②）。架构：七结构插件（vault/log/hot/tag/index/notes/link）+ 五命令（check/ingest/save/query/plugin）+ 协议工件（`.meta/protocol/`）+ 机械脚本（`.meta/scripts/`：plugin_cli 五合一 + wikilib 承重件 + 附检 audit）。分工定则：确定性走脚本，语义走 LLM。规范 doc 后置；user-write/ 为用户手稿（agent 只读）。

## 阶段

① 架构与原型（✓）→ ② 真实操作验证（ingest/check 首轮，暴露盲点并修）→ ③ 规范蒸馏（从原型回写 docs）→ ④ 普世化（新实例复制）→ ⑤ 个人库回填（须用户指令）。当前：②（地基已就绪待验证）。

## 下一步

- 往 vault/ 放入首批资产，跑 ingest 全链路 + check 首审（重点验证：锚点读取、预览前置、滚动触发）
- 观察项：词表复用率、检索 log 行、stub 老化告警是否如预期
- 后续插件按依赖序：trust 时效 → 问题队列 → 画像 / todo（薄）；规范蒸馏与 README 随后

## 过往操作

- 2026-09-09 附检机制（两提交）：audit 发现式执行插件 scripts/check.py（check(ctx) 契约、只读零副作用），在场即注册、不做文本拼接；wikilib 承重件单次扫描共享 ctx.pages；tag/vault 示例过阴性测试；解析器加固；check 机械项移交脚本，注入区块保留语义项

- 2026-09-09 装卸机械化（三提交）：plugin_cli（validate/inject/registry/deploy/all，幂等）+ plugin 命令 + check 接入；manifest 增 inject 成七字段；执行原则定为「确定性走脚本、语义走 LLM」

- 2026-09-09 地基落地（四提交）：① registry + actions 协议工件与 manifest fields 声明；② link 插件新立（孤儿检查自 notes 移交）；③ ingest/save/query 锚点 + 滚动 + 预览前置 + 检索信号；④ check 升级（值集越界/断链/动作分级修复）。设计依据：个人库 128 页取证（哈希失配 40%、积压 41%、status 九值、hot 超规 50 倍、lint 停摆等）

- 2026-09-08 对齐现状：AGENTS.md 改写（框架+原型双定位、原型先行准则、指针更新），log 阶段重写；docs/00 用户精简一并入库

- 2026-09-08 原型落地：原 wiki 思想转化为六结构插件（vault/log/hot/tag/index/notes）与四命令（check/ingest/save/query，lint 并入 check），.meta/ 主本 + .agents/skills/ 部署副本 + AGENTS.md 注入区 + wiki 种子就位；doc 后置，user-write 未动，个人库只读

- 2026-09-07 插件规范草案：协议讨论（manifest / scope / 依赖 / 生命周期 / 合规检查）应用户要求写入 user-write/2.md；先前误落的 .meta/plugins/test/ 实体已撤（自检脚本留存于提交 959f353）

- 2026-08-28 00 状态对齐：docs/00 frontmatter draft→final，闭合与 README「已定稿」、宪法上游定位的口径不一致

- 2026-08-28 撤销骨架定稿：应用户决定保留工作区回退（删 docs/01、log 同步回退）；AGENTS.md 指针、docs/00 §七、README 引用一并同步；旧版见提交 cb09895

- 2026-08-28 初始化：清空旧副本内容（保留 .git）；AGENTS.md、log.md、.gitignore、目录结构就位；三个骨架分叉经用户授权代裁（代理层双目录 sources+notes；raw 归档区子结构实例自定；hot 预留位默认开），写入 docs/01；首次提交
- 2026-08-28 重定位：工程由「个人库副本」转为「普世 vault-wiki 框架」；写入 README、docs/00-principles
- 2026-08-26 前身：作为个人库结构副本建立（沙箱用途）
