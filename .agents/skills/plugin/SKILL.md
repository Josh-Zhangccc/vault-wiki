---
name: plugin
owner: framework
description: "插件生命周期管理：装/升/卸/清单。机械步骤（合规、依赖、注入区、注册表、副本同步）由 .meta/scripts/plugin_cli.py 执行，agent 只做语义部分。Triggers on: plugin, 插件, 装插件, 卸插件, install plugin, uninstall plugin."
---

# plugin：插件装卸

框架的自管理命令。机械步骤全部走脚本，agent 只做语义部分（插件主体内容、变更记录审读、流程冒烟）。生命周期规则源自 user-write/2.md 草案：装卸前必过自检，被依赖者卸载阻断。

## 涉及结构

写：`.meta/plugins/<id>/`（装卸）、AGENTS.md 注入区、`.meta/protocol/registry.yaml` 插件段、`.agents/skills/` 命令副本、wiki/log.md（以上四处投影均经脚本）
读：全部 manifest、`.meta/scripts/plugin_cli.py`

## 装 <id>

1. 准备 `.meta/plugins/<id>/`：
   - PLUGIN.yaml 七字段：id / version / depends / updated / attachment / fields / inject——`inject` 即注入区投影行（一行中文，卸装由脚本同步进 AGENTS.md）
   - PLUGIN.md 结构：职责 → 结构 → 不变量 → 检查 → 注入 → 附件 → 变更记录
2. `python .meta/scripts/plugin_cli.py validate` —— 合规与依赖检查，错误阻断
3. `python .meta/scripts/plugin_cli.py all` —— 注入区 / registry / 命令副本同步
4. 流程冒烟：`python .meta/scripts/plugin_cli.py audit <id>`（如插件带附检脚本）+ 按新插件 PLUGIN.md 的关键流程对测试资产走一遍（草案三级检查之行为层）
5. wiki/log.md 置顶追加一行（类型「装卸」）

## 升 <id>

1. 修改插件；manifest `version` 进位、`updated` 刷新；PLUGIN.md 变更记录加一行
2. `python .meta/scripts/plugin_cli.py all` —— validate + 注入块版本号同步
3. wiki/log.md「装卸」行

## 卸 <id>

1. `python .meta/scripts/plugin_cli.py validate` —— 有插件依赖它 → 阻断（除非用户显式级联）
2. 目录移出 `.meta/plugins/`（归档留存；物理删除永远属人）
3. `python .meta/scripts/plugin_cli.py all` —— 注入区 / registry 中随之消失
4. wiki/log.md「装卸」行

## ls

- `python .meta/scripts/plugin_cli.py ls`（清单 + 依赖）

## 边界

- 脚本只碰四处：插件目录进出、注入区标记块、registry 插件段、命令副本；protocol / reserved 段与 AGENTS.md 手写区永不动
- 附检契约（可选）：`scripts/check.py` 定义 `check(ctx)`，返回 issue 列表（级别 + 消息），只读零副作用，中文消息、无第三方依赖；ctx.root = 仓库根，ctx.pages = 单次扫描的 wiki 页面集
- 卸载归档与删除分离：移出 = 卸，删除属人
- 脚本输出的错误一律阻断操作，修复后重跑；警告（如孤儿副本）仅报告
