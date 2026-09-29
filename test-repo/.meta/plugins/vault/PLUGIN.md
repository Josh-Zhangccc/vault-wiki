# vault：默认域（概念）

domain 的第一个实例：vault 是容纳真实资产的仓库——任意格式（md / txt / csv / pdf / 图像 / 音视频……）原样进入，完整性以哈希登记。双重角色：自身是本地文件域，兼作他域按需落地的通用资产仓储（`url` 字段即借道接口）。本插件是概念声明：只阐述 vault 是什么、立什么规矩；映射法则归 mapping，布局规约归 structure，域契约归 domain。

## Structure

无自有结构与脚本；外领地即根目录 `vault/` 容器本身，wiki 侧属地 `wiki/vault/`（属地惯例归 mapping）。

## Invariants

- 命令侧对 vault 只增：agent 写入只产生新文件，不修改既有文件
- 删改自由属于人：删除、修改、移动是人的权利，命令不执行
- 原文不可变是信任的根基：代理与索引皆可再生，唯原文是唯一真相

## Changelog

- 0.5（2026-09-22）域化：depends 增 domain（默认域定位）与 wiki（属地声明 `wiki/vault/`）；双重角色说破——兼作他域落地仓储，url 字段即借道接口
- 0.4（2026-09-14）治理三块认领完毕：来源保全——认领 registry 预留段 `url`（URL 型资产出处登记，写入契约在 mapping usage）；结构规约——移交 structure 插件（0.1 立设）；生命周期/变更传导——归 mapping（引用计数、重算留痕）与 check（分诊）协作
- 0.3（2026-09-13）注入源移交 manifest：删 Checks / Inject / Attachments 节，md 回归纯文档
- 0.2（2026-09-13）纯化：删对 mapping / check 的职能引用，规矩自足
- 0.1（2026-09-12）立设：概念声明插件（治理后置——来源保全、结构规约、生命周期建议待真实使用后认领）
