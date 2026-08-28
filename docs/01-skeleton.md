---
type: design
status: stable
created: 2026-08-28
updated: 2026-08-28
---

# 骨架最小集与目录结构（v1.0 定稿）

> 2026-08-28 定稿。三个分叉由用户授权 agent 代裁，裁决及理由记录于文末。

## 目录结构（实例骨架）

```
vault/
├── AGENTS.md                  # 实例宪法：近全通用 + 指向 .vault-meta/ 的实例指针
├── docs/
│   ├── README.md              # 准则注册表（未登记视为不存在）
│   └── conventions/           # 通用准则集，按流水线工位分篇
├── raw/
│   ├── inbox/                 # 前门：一切新文件的唯一入口（人类采集区）
│   └── …                      # 归档区：子结构实例自定
├── wiki/
│   ├── sources/               # 解析工位产出（代理契约：raw_file + sha256）
│   ├── notes/                 # 沉淀工位产出（类型在 frontmatter）
│   ├── index.md               # 索引工位：总目录
│   ├── log.md                 # 运营：append-only 操作日志
│   └── hot.md                 # 热缓存（增强件，默认开启）
├── .agents/skills/            # 技能薄壳（路由 + 读准则）
├── scripts/                   # lint、格式解析器
└── .vault-meta/               # 实例配置层：个性化所在
```

## 最小集清单

**核心件**（没有它不成 vault）：`raw/` + inbox 前门；`wiki/sources/` + 代理契约；`index.md` 与 `log.md`；实例宪法 + `docs/conventions/`；`.vault-meta/` 空模板。

**增强件**（骨架预留位，实例选用）：`hot.md`（默认开）、`.agents/skills/`、`scripts/`、QUESTIONS.md 开放问题队列。

两条试金石：「没有它还能不能叫 vault」定核心件；「搬不进一个全新实例的就是个人层」剔个人内容。

## 分叉裁决记录（2026-08-28）

1. **代理层目录学 → B 双目录**：`sources/`（解析产物，必带 raw_file + sha256）+ `notes/`（沉淀产物，类型放 frontmatter：concept / entity / comparison / session 等，聚合靠 index 或 Bases）。理由：目录只反映流水线两个产出，类型是数据模型可自由扩展，两条代理契约天然分工。session 转录视为一种 source（type: session），不单设目录。
2. **raw/ 归档区子结构 → 骨架不规定**：只立三条规则——一切新文件经 `raw/inbox/` 进入；归位属移动而非修改内容；完整性以哈希登记。子目录归实例配置，实例可将部分子目录（如 Diary/）声明为额外采集区。
3. **hot.md → 增强件**：骨架预留位、默认开启。冷启动优化件，没有它 agent 仍可经 index 引导。
