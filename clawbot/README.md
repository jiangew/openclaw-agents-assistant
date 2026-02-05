# Clawbot (Discord)

## 结构
- `clawbot.py` 启动入口
- `clawbot.config.json` 默认配置（位于项目根目录）
- `clawbot.config.local.json` 本地覆盖（位于项目根目录，可选）
- `cogs/commands.py` 命令集合
- `cogs/listeners.py` 事件监听

## 快速开始
```bash
python clawbot/clawbot.py
```

## 配置
默认读取 `clawbot.config.json`，若存在 `clawbot.config.local.json` 会覆盖同名字段（适合本地私密配置）。
`discord_token` 必须在配置文件中提供。

示例：`config.local.json`
```json
{
  "discord_token": "YOUR_TOKEN_HERE",
  "bot_prefix": "!",
  "allowed_guilds": [123456789012345678],
  "keywords": ["btc", "eth"],
  "enable_reactions": true,
  "log_level": "INFO",
  "admin_user_ids": [111111111111111111],
  "admin_role_ids": [222222222222222222],
  "admin_only_commands": ["reload"]
}
```

## 运行示例
```bash
python clawbot/clawbot.py
```

## 权限与管理
- `admin_user_ids` 和 `admin_role_ids` 用于管理权限
- `admin_only_commands` 列表中的命令仅管理员可用

## 热重载
管理员可执行：`!reload` 或 `!reload <cog>`（如 `!reload commands`）
