# lark-im：人际域

以 lark-cli 为接口的人际档案层：群档 + 人档。人是关系的锚，不是档案行——wiki 存的是人际版图（有哪些群、跟谁打交道、议题结论），不是消息记录，也不是通讯录镜像（roster 全量属「全量映射禁」的 im 版，且 contact 域只解析不遍历）。基座档案页分区制（0.2）为本域前提。

## Structure

- `<profile>/im.md`（kind: im）——域枢纽：frontmatter `im` 块映射 = 策略（键如 群同步 / 涌现 / 关注 / 排除，值一句话）；人档涌现条件在此声明
- `<profile>/im/chats/<群名>.md`（kind: chat）——群档：frontmatter 机械区（`lark` 身份字段 + `description` 群功能一句话 + `key_members` 关键人 wikilink）；正文沉淀区 = 议题记录，append-only（`## YYYY-MM-DD 议题：X → 结果：Y`），按需写入
- `<profile>/im/people/<姓名>.md`（kind: person）——人档：token = open_id（app 内稳定）；基本信息 `department` / `position`（contact 解析填充）；`chat_id` 为 p2p 单聊锚（一人一档吃掉 p2p 页，无单聊则缺省）；正文沉淀区 = 与我的关系（主观、只增收敛）
- 目录两分 chats/ people/；文件名机械清洗（非法字符、emoji），重名加短 token 尾缀

## Invariants

- 人档涌现制：p2p 单聊过 / 用户点名（枢纽关注清单）/ 高频交互——条件写枢纽策略块，不做全员建档；群参与人不存全名单，只存关键人（群主必在，余为已建档者，wikilink 指向人档）
- 群档对账走 lark-map：`im +chat-list` 全量枚举 → token↔页 diff → 建档（群功能蒸馏 + key_members 群主起步）/ 改机械区 / 退群标 `status: deprecated`；人不枚举
- 议题记录按需：谁问谁拉（时间窗 + contact 翻译人名 + threads 展开话题楼），蒸馏成节**经用户确认后追加**；默认零消息正文
- 发送 / 回复 / 加急等写面操作永远须用户明示，lark-map 只读
- 隐私红线：关系描述等主观内容属实例数据，不入框架仓库与 test-repo（demo 用假人）
- trust lazy-refresh 同基座（TTL 默认 7 天，身份页可覆写）

## Changelog

- 0.1（2026-09-19）立设：群档 / 人档目录两分 + 涌现制（策略入枢纽）+ 关键人制 + 议题按需沉淀
