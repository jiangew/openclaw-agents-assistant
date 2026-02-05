# MEMORY.md - 稳定记忆与契约

## FILE_CONTRACTS
- INPUT_MARKETS: polymarket.csv
- INPUT_KOLS: x_feed.txt
- OUTPUT_PRIMARY: analysis_report.md

## ANALYSIS_RULES
- 对比：市场情绪 vs KOL 叙事
- 产出：趋势判断 + 风险提示 + 分歧点
- 不做投资建议，仅描述倾向与风险

## RISK_FRAMEWORK
- 监管与合规
- 安全与合约风险
- 流动性与交易深度
- 叙事错配与情绪反转

## SIGNAL_RULES
- 市场情绪：基于高流动性/高成交量市场的方向
- KOL 情绪：基于高互动/明确立场内容
- 若两者方向相反，标记为“高分歧”

## FILTER_RULES
- 不基于广告/促销型内容做结论
- 仅使用最近 30 天内的数据（若可判定时间）
- 不足样本则输出“样本不足”

## INSTITUTION_WATCHLIST
- ARK Invest / Cathie Wood
- Strategy (MicroStrategy) / Michael Saylor
- BitMine
- Circle
- Robinhood
- Coinbase
- OKX
- Binance
- OSL Group
- Yunfeng Financial
- 美股矿池/矿企

## KOL_FOCUS
- elonmusk
- VitalikButerin
- CathieDWood
- michaeljburry
- cz_binance
- starxu
- ChrisLee
- DiscussFish
- saylor

## TOPIC_LAYERS
- 稳定币: USDT, USDC, DAI, Tether, Circle
- 监管: SEC, CFTC, MiCA, CBDC, policy

## WARNINGS
- 

## CHANGES
- 2026-02-04: 初始化记忆模板
- 2026-02-04: 输入文件对齐为 polymarket.csv 与 x_feed.txt
- 2026-02-04: 增加分析信号与过滤规则
- 2026-02-04: 增加机构/KOL关注清单与稳定币/监管分层
