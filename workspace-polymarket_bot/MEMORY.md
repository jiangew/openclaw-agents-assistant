# MEMORY.md - 稳定记忆与契约

## FILE_CONTRACTS
- OUTPUT_PRIMARY: polymarket.csv

## MARKET_SCOPE
- Section: Crypto
- Include: 主流币价格目标、宏观事件、重大政策/监管、稳定币相关

## SORT_RULES
- Primary: 流动性
- Secondary: 交易量

## FORMAT_RULES
- 统一日期格式：YYYY-MM-DD
- 货币统一为 USD

## MARKET_KEYWORDS_INCLUDE
- BTC, Bitcoin, ETH, Ethereum, SOL, Solana, XRP, ADA, BNB, DOGE
- stablecoin, USDT, USDC, DAI, Tether, Circle
- SEC, CFTC, regulation, policy, MiCA, CBDC
- ETF, approval, spot ETF, inflows, outflows
- macro, CPI, rates, recession, liquidity

## MARKET_KEYWORDS_EXCLUDE
- sports
- election
- celebrity
- weather
- entertainment

## QUALITY_RULES
- 只保留 Crypto 相关市场
- 排名不足 20 时写明原因
- 缺失赔率/截止日期时标注为 `NA`

## WARNINGS
- 

## CHANGES
- 2026-02-04: 初始化记忆模板
- 2026-02-04: 输出文件对齐为 polymarket.csv
- 2026-02-04: 增加包含/排除关键词与质量规则
- 2026-02-04: 稳定币/监管关键词分层
