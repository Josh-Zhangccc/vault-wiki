---
name: asset-read
owner: framework
description: "按路径取任意格式资产的文本（md 直读 / pdf 经 PyMuPDF / docx 与 xlsx 标准库解包），产物缓存 wiki/tmp 并标 stale_after——回源读取的统一通道与缓存惯例。Triggers on: asset-read, 读资产, 回源, 提取文本, 读课件原文, read asset."
---

# asset-read：资产回源读取

按路径读取任意格式资产的文本——回源的统一通道：vault 资产、bb/ 拉取物、库外相对路径皆可。读取是登记的增强而非替代：代理页一行描述管概览，深问才回源。

## Scope

读：任意格式资产（wiki 外文件系统，只读）
写：`wiki/tmp/` 提取缓存（唯一落点）

## Steps

1. 定位资产路径与扩展名；md / txt / csv 直读即毕，不落缓存
2. 查缓存：`wiki/tmp/<资产名>.txt` 在场且未过 stale_after → 直读缓存，不重抽
3. 未命中则提取：
   - pdf：PyMuPDF（`import fitz`；缺失先 `pip install pymupdf`）；大文件按页区间或关键词定位抽取，不整本进上下文
   - docx / xlsx：纯标准库 zipfile + xml 文本节点提取
   - 其他二进制：不深读，如实报「不支持文本提取」
4. 产物落 `wiki/tmp/<资产名>.txt`，文件头三行注释：源路径 / 提取日 / stale_after = 提取日 + 7 天
5. 回报要点与出处（页码或节名）

## Prohibitions

- 不修改资产原件（只读纪律随所在域不变）
- 禁全量批量提取——按需单件；一次性查看不落缓存
- 缓存过期由 check 报清单、处置经确认（tmp 插件既有规则，本命令不自行清理）

## Language

中文为主，资产原文语言保留原形。

## Parameters

- 资产路径（根相对）；可选页区间或定位关键词
