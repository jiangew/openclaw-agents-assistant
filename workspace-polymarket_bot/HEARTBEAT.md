# HEARTBEAT.md - 主动机制

- 检查 `polymarket.csv` 是否超过 6 小时未更新
- 若过期：刷新 Crypto Top20 并写回
- 必须补齐 `price` 与 `expiry` 与 `link`；若缺失，写入 failures 并标注需要重抓
- 若抓取失败：在 `polymarket.csv` 的 `# Meta` 末尾追加失败原因与下次建议
- 发现站点结构变化：记录到 `MEMORY.md` 的 WARNINGS
