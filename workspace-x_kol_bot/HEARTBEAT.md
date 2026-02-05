# HEARTBEAT.md - 主动机制

- 检查 `x_feed.txt` 是否超过 6 小时未更新
- 若过期：刷新 KOL 最新内容并写回
- 必须补齐 `source` URL；若缺失，写入 failures 并标注需要重抓
- 若抓取失败：在 `x_feed.txt` 的 `# Meta` 末尾追加失败原因与下次建议
- 发现 KOL 改名/失效：记录到 `MEMORY.md` 的 WARNINGS
