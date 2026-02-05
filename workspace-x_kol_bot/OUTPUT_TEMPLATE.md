# OUTPUT_TEMPLATE.md - x_feed.txt

Spec: `workspace/OUTPUT_SPEC.md` v1.2

## 格式
- 纯文本
- 每行一条：`[YYYY-MM-DD] 类别: 内容 (source: <url>)`
- 末尾追加 `# Meta` 区块

## 类别枚举
- `INSIGHT`
- `ALERT`
- `BULLISH`
- `BEARISH`
- `NEUTRAL`

## 模板
```
[YYYY-MM-DD] INSIGHT: <简要内容> (source: <url>)
[YYYY-MM-DD] ALERT: <简要内容> (source: <url>)
[YYYY-MM-DD] BULLISH: <简要内容> (source: <url>)
[YYYY-MM-DD] BEARISH: <简要内容> (source: <url>)
[YYYY-MM-DD] NEUTRAL: <简要内容> (source: <url>)

# Meta
- spec_version: 1.2
- time_range: <YYYY-MM-DD..YYYY-MM-DD>
- kols: <数量> / <名单概要>
- filters: <命中主题与黑名单摘要>
- duplicates_removed: <数量>
- failures: <如有>
```
