# OUTPUT_TEMPLATE.md - polymarket.csv

Spec: `workspace/OUTPUT_SPEC.md` v1.2

## 格式
- CSV
- 表头固定：`rank,title,price,volume,liquidity,expiry,link`
- 末尾追加 `# Meta` 行

## 模板
```
rank,title,price,volume,liquidity,expiry,link
1,"<market title>",<price>,<volume>,<liquidity>,<YYYY-MM-DD>,<url>
2,"<market title>",<price>,<volume>,<liquidity>,<YYYY-MM-DD>,<url>
...
# Meta
# spec_version: 1.2
# time_range: <YYYY-MM-DD..YYYY-MM-DD>
# scope: Crypto
# sort: liquidity desc, volume desc
# total_rows: <n>
# failures: <如有>
```
