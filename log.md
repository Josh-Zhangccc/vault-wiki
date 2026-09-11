# 项目日志

> 追加与修改须标注日期（精确到天）；总量 <2k 字；整合压缩须用户同意。

## 现状（2026-09-11）

工程处于原型验证期（阶段②）。架构：九结构插件分三层（origin：vault/notes/sessions；field：tag/link/trust；derived：index/hot/log，依赖方向由 plugin_cli 校验）+ 五命令（owner×commands 双向绑定：vault→ingest、notes/sessions→save，check/query/plugin=framework）+ 协议工件 + 双脚本（plugin_cli 生命周期；pipeline 写后管道 index/tags/hot/log/verify）。已对齐 OKF v0.2（status 三值、信任字段已由 trust 认领、actor 约定、渐进披露索引、归档改轨）；写后自证入纪律。附检覆盖 6/9 插件（vault/tag/sessions/trust/link/log），check 注入块由 plugin_cli 自 PLUGIN.md 检查节机械化投影。规范 doc 后置；user-write/ 为用户手稿（agent 只读）。

## 阶段

① 架构与原型（✓）→ ② 真实操作验证（ingest/check 首轮，暴露盲点并修）→ ③ 规范蒸馏（从原型回写 docs）→ ④ 普世化（新实例复制）→ ⑤ 个人库回填（须用户指令）。当前：②（地基已就绪待验证）。

## 下一步

- 往 vault/ 放入首批资产，跑 ingest 全链路 + check 首审（重点验证：写后管道与 verify 自证、锚点读取、预览前置）
- 观察项：词表复用率、检索 log 行、stub 老化告警、verify 误报率；notes type→frontmatter 模板等首轮 save 漏写率实证；sessions 形状随首轮真实 save 校准

## 过往操作

- 2026-09-11 提交纪律入动作纪律（actions.md 姊妹节）：数据区写入首次有提交规则——一次写操作=一提交、verify 过才提交、信息 `摄入:/保存:/检查:`、agent 只 add 自写路径（禁 add -A，人写变更提交权属人）；ingest/save/check 管道尾部随行指针；裁决不立 git 插件（过程层非结构，lockfile/审计/历史检索维持协议引用）

- 2026-09-11 优化三件落地（用户裁定「均可执行」）：① trust 插件立设（field 层，认领 registry 预留四字段 generated/verified/stale_after/sources 回填插件段；层级推导不落盘；附检契约+stale 清单+信任水位，日历非法日期加固）；② 机械项收编附检——link（断链/乱码/孤儿/别名二义 error/related 单向信息）、tag（层级深度）、log（日期契约），附检覆盖 6/9；③ check 注入块机械化（plugin_cli 自 PLUGIN.md 检查节投影，幂等，在场即注册），手写块与源头的漂移通道关闭
- 2026-09-11 命令-插件绑定显式化（三提交）：manifest 增可选 commands、命令 frontmatter 增 owner（save=notes+sessions 双主；check/query/plugin=framework 跨切面显式无主），plugin_cli 校验无主/孤儿/单边 + ls 增命令列（正反测试通过）；user-write 两份手稿经隐私核查首次入库；smoke-tmp 冒烟遗留清理并 gitignore

- 2026-09-10 sessions 独立插件立设（结构归位，命令回纯操作）：领地 `wiki/sessions/`（准则 3 目录枚举随改：代理层 + 原生区两分）；participants 字段用 actor 约定留多 agent 扩展点；附检（领地边界 / 契约）；notes 缩界 0.5（会话移出）；save 会话段移交插件、类型表去复读；multiagents 不预立（sessions 的演化方向）

- 2026-09-10 分层与 OKF 对齐落地（七提交）：插件分 origin/field/derived 三层 + plugin_cli 依赖方向规则；registry 对齐 OKF v0.2（status=draft/stable/deprecated、预留 generated/verified/stale_after/sources、actor 约定、description 推荐）；link 断链降级 warning + 孤儿作用域明文；log 归档改轨 archive/月/log.md；index 每目录化（渐进披露，根页带 okf_version）+ vault 豁免 index.md；新增 pipeline.py 写后管道（index/tags/hot/log/verify=attester 最小形），命令尾部接管道 + generated 署名；OKF 冒烟通过（viz.html 渲染成功，反链/信任字段可显）

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
