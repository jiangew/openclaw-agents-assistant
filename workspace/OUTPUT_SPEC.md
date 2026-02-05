# OUTPUT_SPEC.md - Unified Output Specification

Version: 1.2
Date: 2026-02-04

## Global Rules
- 所有输出必须可追溯（包含时间与来源链接）
- 不足项必须明确标注（不得编造）
- 统一时间格式：`YYYY-MM-DD`（如有时分可用 `YYYY-MM-DD HH:mm`）
- 版本化：每个输出必须声明 `spec_version` 且等于本规范版本
- 若缺少关键字段（source/expiry/link），必须在 failures 中标注并触发重抓

## x_kol_bot (x_feed.txt)

### Fields
- date: `YYYY-MM-DD`
- category: `INSIGHT | ALERT | BULLISH | BEARISH | NEUTRAL`
- content: 简洁摘要（单句优先）
- source: 原帖 URL

### Line Format
`[YYYY-MM-DD] CATEGORY: <content> (source: <url>)`

### Meta Block
- spec_version: 当前规范版本
- time_range: 数据覆盖范围
- kols: 覆盖 KOL 数量与概览
- filters: 命中主题与黑名单摘要
- duplicates_removed: 去重数量
- failures: 抓取失败/不足项

### Example
```
[2026-02-04] INSIGHT: ETH ETF inflows rose for the third day. (source: https://x.com/...)

# Meta
- spec_version: 1.2
- time_range: 2026-02-03..2026-02-04
- kols: 6 / VitalikButerin, CathieDWood, cz_binance...
- filters: stablecoin, regulation
- duplicates_removed: 3
- failures: none
```

## polymarket_bot (polymarket.csv)

### Header
`rank,title,price,volume,liquidity,expiry,link`

### Field Rules
- rank: 1..20
- price: 0-1 概率或价格（缺失用 `NA`）
- volume/liquidity: USD 数字（缺失用 `NA`）
- expiry: `YYYY-MM-DD`（缺失用 `NA`）
- link: 市场 URL

### Meta Lines
以 `# ` 开头：
- spec_version
- time_range
- scope
- sort
- total_rows
- failures

### Example
```
rank,title,price,volume,liquidity,expiry,link
1,"Will ETH be above $3,500 on Feb 10?",0.62,25000,41000,2026-02-10,https://polymarket.com/...
# Meta
# spec_version: 1.2
# time_range: 2026-02-04..2026-02-04
# scope: Crypto
# sort: liquidity desc, volume desc
# total_rows: 20
# failures: none
```

## crypto_analyst (analysis_report.md)

### Required Sections
- Summary
- Market vs KOL
- Divergences
- Major Coins
- Risks
- Watchlist (24-72h)

### Spec Version Line
- 在头部声明：`Spec: 1.2`

### Evidence Rule
- 至少 1 条结论要明确引用 `polymarket.csv` 与 `x_feed.txt` 的具体行/市场标题

### Example (Skeleton)
```
# Sentiment Analysis Report
Date: 2026-02-04
Data Window: 2026-02-03..2026-02-04
Sources: polymarket.csv, x_feed.txt
Spec: 1.2

## Summary
- ...

## Market vs KOL
- Market: ...
- KOL: ...
- Evidence: ...

## Divergences
- ETH: bullish vs cautious | Confidence: high

## Major Coins
- BTC: ...
- ETH: ...
- Stablecoins: ...

## Risks
- ...

## Watchlist (24-72h)
- ...
```
