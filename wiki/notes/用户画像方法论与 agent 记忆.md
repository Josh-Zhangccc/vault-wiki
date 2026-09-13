---
type: concept
title: 用户画像方法论与 agent 记忆
description: 画像两条资料线的收敛——产品设计线的维度框架与 agent 记忆线的更新机制，及 vault-wiki 画像插件的选型依据
created: 2026-09-13
updated: 2026-09-13
generated:
  by: agent/GLM-5.3
  at: 2026-09-13
tags:
  - 画像/方法论
  - agent-memory
---

# 用户画像方法论与 agent 记忆

「用户画像」有两条实践线，语义不同：产品设计线画的是**虚构目标用户代表**（persona），为设计决策服务；agent 记忆线维护的是**对真实使用者的持续认知档案**（user profile），为个性化服务服务。vault-wiki 的画像插件属后者——维度框架借前者，更新机制借后者。

## 产品方法论的维度框架

主流 persona 模板字段收敛为：基本属性、角色/背景、目标、痛点、行为习惯、动机。中文资料普遍区分**静态维度**（人口属性，低频变更）与**动态维度**（行为偏好，持续演进）。构建流程为三步框架：获取与研究用户信息 → 细分用户群 → 建立与丰富画像。

两条实用纪律：

- **不服务决策的细节就该丢弃**——画像不是越全越好，是不能行动的细节都不要。
- **画像有长久性要求**——会过时，必须持续维护；静态/动态分层正好对应不同的更新频率与过期策略。

## agent 记忆的更新机制

agent memory 领域的核心模式：画像由**静态身份事实 + 实时行为信号**两层构成；user-scoped 持久记忆支撑跨会话连续性；画像随用户反馈增量更新。行为信号与自述信号互补——用户做了什么（放入哪些资产）常比用户说了什么更硬。

## vault-wiki 的选型

画像页为收敛式认知档案：静态身份层 + 动态偏好层，分节开放、维度不枚举。断言必带证据 wikilink（防幻觉堆积），偏好层挂 stale_after（会过时的知识显式声明过期时刻）。信号双通道：对话保存（自述信号）与资产映射（行为信号）。零自有字段，信任留痕全复用 trust 语义。

## 来源

- 知乎专栏「数据分析之用户画像方法与实践」、人人都是产品经理「构建用户画像的流程与方法」、boardmix「persona 的 8 个内容维度」——维度与流程线
- Supermemory「How AI User Profiles Drive Personalization」、Mem0「Build an AI Agent That Actually Remembers Your Users」、Microsoft Foundry user-scoped persistent memory——agent 记忆线
