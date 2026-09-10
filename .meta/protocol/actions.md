# 动作纪律：路径分区 × 动作分级

> 权限的语义形态：本表不依赖代码做「强制」，但确定性的结构操作交给脚本（`.meta/scripts/plugin_cli.py`：合规 / 依赖 / 注入 / 注册表 / 副本同步；`.meta/scripts/pipeline.py`：index / tags 重建、hot / log 滚动、写后自证），语义判断交给 LLM；agent 执行前对照本表，check 以脚本与 git 痕迹事后审计。
> 四条执行原则：确定性结构操作走脚本、语义判断走 LLM；规则明文写出「怎么做」而非「是什么」；一次读取够用的不做第二次扫描（调用节俭）；写命令收尾必过 `pipeline.py verify` 自证（attester 最小形：LLM 执行、脚本认证）。

## 路径分区

| 分区 | 路径 | 性质 |
|---|---|---|
| 可再生 | `wiki/index.md`、`wiki/tags.md`、`wiki/hot.md`、`.meta/protocol/registry.yaml` 插件段 | 派生投影，可整体重建，管道随便重跑 |
| 珍贵 | `wiki/notes/**`、`.meta/plugins/**`、`.meta/command/**`、AGENTS.md 手写区 | 只增或人改 |
| 不可变 | `wiki/log.md` 与 `wiki/log-archive/**` 的既有条目、`vault/**`（命令视角） | 写入后内容不得改写 |

## 动作分级

| 级别 | 典型动作 | 执行方式 |
|---|---|---|
| 机械自动 | 索引 / tags / 注册表重建、注入区重建、hot 窗口淘汰、log 归档分流、哈希重算、检索 log 行、命令副本同步、写后自证 | 直接执行（脚本能做的走脚本：`plugin_cli.py` 与 `pipeline.py`），不询问 |
| 机械确认 | tag 合并（批量改插件字段）、预留字段迁移 | 呈清单，确认后执行 |
| 语义报告 | 笔记合并建议、近重复提示、代理描述失效判断 | 报告差异，人决定 |
| 永远属人 | 删除、历史改写、`vault/` 既有文件改动、笔记正文改写 | 命令不执行；用户显式指令的代笔须 log 留痕 |

判据：改的是「插件拥有的字段或可再生页」→ 机械；动「正文或既有历史」→ 人。

## 滚动机制（明文）

- **log**：主文件窗口 ≤100 条（约 14k 字符）。写 log 走 `pipeline.py log <类型> "<一句话>"`——超限自动把最旧一段按条目月份分组搬入 `wiki/archive/YYYY-MM/log.md`，条目内容一字不改、只搬位置；归档目录落入不可变区
- **hot**：≤25 条、<5 日、单条 ≤200 字符。写 hot 走 `pipeline.py hot <类型> "<一句话>"`——写前自动淘汰越界条目、截超长条目
- **索引 / 注册表**：与实际偏差 → check 中直接重建（`pipeline.py index` / `tags`；`plugin_cli.py all`），不询问
- **词表**：ingest / save 写 tags 前先读 `wiki/tags.md`（派生区即词表），优先复用既有词；近重复合并是机械确认项
- **参数属主**：滚动窗口等机械参数以 `pipeline.py` 源码为准（脚本源码即规则清单），插件 PLUGIN.md 保留语义说明——命令与文档不复抄数字
