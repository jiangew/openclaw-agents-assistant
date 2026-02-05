# OUTPUT_TEMPLATE.md - analysis_report.md

Spec: `workspace/OUTPUT_SPEC.md` v1.2

## 格式
- Markdown

## 模板
```
# Sentiment Analysis Report
Date: <YYYY-MM-DD>
Data Window: <YYYY-MM-DD..YYYY-MM-DD>
Sources: polymarket.csv, x_feed.txt
Spec: 1.2

## Summary
- <3-5 bullets>

## Market vs KOL
- Market: <overall tone>
- KOL: <overall tone>
- Evidence: <key rows or lines>

## Divergences
- <asset/topic>: <market view> vs <KOL view> | Confidence: <low/med/high>

## Major Coins
- BTC: <trend> | Drivers: <2-3>
- ETH: <trend> | Drivers: <2-3>
- Stablecoins: <trend> | Drivers: <2-3>

## Risks
- <regulation>
- <security>
- <liquidity>
- <narrative mismatch>

## Watchlist (24-72h)
- <event/market/topic>
```
