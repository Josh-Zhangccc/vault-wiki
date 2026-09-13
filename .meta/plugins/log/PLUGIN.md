# log：运行日志

库的操作流水：什么时候对库做了什么。只增不删的历史，与 hot（会淘汰的现在）相对。

## Structure

- 单文件 `wiki/log.md`，条目置顶追加（最新在最上）
- 条目格式：`- YYYY-MM-DD <类型>：一句话概述`（含 wikilink）
- 类型枚举：map / save / query / check / plugin / other（实例可扩）

## Invariants

- 条目只增不改写（「只增不删」的对象是条目内容，非文件物理位置）；修改历史条目 = error
- 每条必须标日期（精确到天）
- 归档搬移不改动条目内容一字

## Rolling

主文件是滚动窗口，不是无限账本：

- 窗口 ≤100 条（约 14k 字符；机械权威源在 `pipeline.py`，本节为语义说明）
- 写 log 走 `pipeline.py log <类型> "<一句话>"`：超限自动把最旧一段按条目月份分组搬入 `wiki/archive/YYYY-MM/log.md`，条目内容一字不改、只搬位置（归档文件是所在目录的保留名 log.md——保留名文件非概念页，天然豁免 frontmatter）
- 归档目录落入不可变区；压缩整合仍须人确认（见宪法准则 5）

## Config

```yaml config
log.max_entries: 100     # 主文件滚动窗口（条）
log.max_chars: 14000     # 窗口字符上限（约）
```

## Checks

- 机械项（附检脚本 `scripts/check.py`，audit 发现式执行）：无日期条目（`- ` 开头而不匹配日期格式，主文件与归档同检）→ error
- 语义项（check 命令）：历史条目被修改（git 可核）→ error；容量超限 → 机械归档后复查

## Usage

- 写行（机械自动）：`python .meta/scripts/pipeline.py log <类型> "<一句话>"`；滚动窗口与归档由脚本执行

## Inject

AGENTS.md 一行：log 语义与置顶追加规则。

## Attachments

无 wiki 附件；附检脚本 `scripts/check.py`（机械检查项，audit 发现式执行）。

## Changelog

- 0.9（2026-09-13）立「Usage」节：写侧契约交由命令注入区投影（单一文本源）
- 0.8（2026-09-12）manifest 去 layer（废分层：注入序改依赖拓扑+字母序，方向校验撤除）
- 0.7（2026-09-12）标识符英文化：节头 / 附检契约键 / 类型枚举 / 管道调用参数
- 0.1（2026-09-08）自原 wiki log 规则转化
- 0.2（2026-09-09）滚动归档机制明文化（窗口 100 条），类型枚举增「检索」；参数依原库实测校准（条均 139 字）
- 0.3（2026-09-10）manifest 增 layer: derived（分层立设：派生层，零依赖）
- 0.4（2026-09-10）归档路径改轨 `wiki/archive/YYYY-MM/log.md`（按条目月份分组；保留名豁免 frontmatter）
- 0.5（2026-09-10）写入机械化：走 pipeline.py log（容量检查与归档由脚本执行），参数权威源移交脚本源码
- 0.6（2026-09-11）无日期条目校验收编附检脚本（主文件与归档同检）；历史修改审计留语义项（git 可核）
