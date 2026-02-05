# HEARTBEAT.md - 主动机制

- 检查 `polymarket.csv` 与 `x_feed.txt` 是否超过 6 小时未更新
- 若任一过期：标注需要刷新，避免基于过期数据输出
- 若输入已更新且 `analysis_report.md` 超过 6 小时未生成：自动重算并写回
