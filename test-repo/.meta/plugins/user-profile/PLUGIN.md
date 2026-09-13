# user-profile：用户画像

对使用者的持续认知档案。wiki 借它把「用户是谁、偏好什么」从对话记忆变成可检查的页面：断言带证据、偏好会过期、更新留痕。定位为 agent 记忆线的 user profile（对真实使用者的认知），非产品设计线的虚构 persona——维度框架借前者研究的成果，更新机制借后者。设计依据见 `wiki/notes/用户画像方法论与 agent 记忆`。

## Structure

- `wiki/profile.md`——单页档案，type: profile；静态身份层（称呼、语言、背景）与动态偏好层（题材、风格、习惯）分节开放，维度不枚举（架构不预置字段清单）
- 零自有字段：留痕与信任全复用 trust（generated / verified / stale_after / sources）
- 断言证据 = 正文行内 wikilink，指向会话页（sessions 领地）或 vault 代理页（mapping 领地）——证据结构跨两领地，是本插件 depends 二者的原因；加上出身二分（wiki）与留痕语义（trust）共四依赖

## Invariants

- 收敛式更新：新值取代旧值、正文留痕（单行：谁何时改了什么）——区别于 notes 的只增不改，画像页是全库第一个可更新语义页面
- 断言必带证据 wikilink；单条增量断言不等于偏好，偏好是页内聚合出的模式
- 日记类资产只记元信号（有无、节奏），内容不进画像——豁免随 mapping，隐私红线二次设防
- 隐私红线：画像内容是实例数据，不入框架仓库与 test-repo
- 画像页缺失 ≠ 错误：首建属 wiki 初始化，机制随设计文档定案（独立建构/整合命令同批后置）

## Changelog

- 0.1（2026-09-13）立设：`wiki/profile.md` 收敛式认知档案（type: profile 入 registry 值集）；depends [wiki, trust, mapping, sessions]；双信号通道挂 save / map（consumes 插 trust 后派生前）；检查三项——断言证据闸门（warning）、领地走错（error）、页面缺失（信息级）
