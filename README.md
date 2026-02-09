# Multi-Agents Assistant based on OpenClaw and Discord Bot

A local OpenClaw multi‑agent system for crypto market monitoring, integrated with a Discord bot. It collects KOL signals, prediction market data, and generates structured sentiment analysis reports.

## Architecture
Agents:
- `main`: default orchestrator, routes tasks to sub‑agents.
- `x_kol_bot`: collects high‑signal X (Twitter) KOL posts.
- `polymarket_bot`: collects top crypto markets from Polymarket.
- `crypto_analyst`: compares market vs KOL sentiment and writes the report.

Primary outputs:
- `x_feed.txt`
- `polymarket.csv`
- `analysis_report.md`

Specs and templates:
- `/Users/jiangew/.openclaw/workspace/OUTPUT_SPEC.md`
- `/Users/jiangew/.openclaw/workspace-x_kol_bot/OUTPUT_TEMPLATE.md`
- `/Users/jiangew/.openclaw/workspace-polymarket_bot/OUTPUT_TEMPLATE.md`
- `/Users/jiangew/.openclaw/workspace-crypto_analyst/OUTPUT_TEMPLATE.md`

## Repo Layout
- `/Users/jiangew/.openclaw/openclaw.json` OpenClaw config
- `/Users/jiangew/.openclaw/clawbot/` Discord bot implementation
- `/Users/jiangew/.openclaw/clawbot.config.json` Discord bot config
- `/Users/jiangew/.openclaw/workspace-*` Agent workspaces
- `/Users/jiangew/.openclaw/logs/` Gateway and bot logs

## Discord Bot (clawbot)
Cogs-based bot with config in root.

Run manually:
```bash
/Users/jiangew/.openclaw/.venv/bin/python /Users/jiangew/.openclaw/clawbot/clawbot.py
```

LaunchAgent (daemon) config:
- `/Users/jiangew/Library/LaunchAgents/com.openclaw.clawbot.plist`

Control:
```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.clawbot.plist
launchctl start com.openclaw.clawbot
launchctl stop com.openclaw.clawbot
launchctl unload ~/Library/LaunchAgents/com.openclaw.clawbot.plist
```

## OpenClaw Gateway
Gateway is local with password auth.

Restart:
```bash
openclaw gateway restart
```

## Agent Routing
Current Discord binding routes to `main`:
- `/Users/jiangew/.openclaw/openclaw.json` -> `bindings.agentId = "main"`

From Discord, ask `main` to spawn sub‑agents, for example:
- “启动 x_kol_bot 抓取 X 上的 KOL 内容”
- “让 polymarket_bot 更新 top20 预测市场”
- “用 crypto_analyst 生成分析报告”

## Security Placeholders
Replace secrets with placeholders in docs and configs.

Examples:
- `discord_token`: `YOUR_DISCORD_BOT_TOKEN`
- `gateway_password`: `YOUR_GATEWAY_PASSWORD`
- `api_key`: `YOUR_PROVIDER_API_KEY`

## Architecture Flow (OpenClaw Multi‑Agent)
```mermaid
flowchart TD
  U["User (Discord)"] --> D["Discord Bot (clawbot)"]
  D --> G["OpenClaw Gateway (WS 18789)"]

  G --> GA["Gateway Auth (password)"]
  GA --> GR["Routing Rules (bindings)"]
  GR --> M["main agent (orchestrator)"]

  M --> S1["sessions_spawn"]
  S1 --> XK["x_kol_bot (X/KOL collector)"]
  S1 --> PM["polymarket_bot (market collector)"]
  S1 --> CA["crypto_analyst (sentiment/report)"]

  XK --> XF["x_feed.txt"]
  PM --> PC["polymarket.csv"]
  XF --> CA
  PC --> CA
  CA --> AR["analysis_report.md"]

  AR --> QG["Output Quality Gate (validate_outputs.py)"]
  QG --> OK["Pass/Fail"]
```

## Local Development
Create venv and install dependencies:
```bash
python3 -m venv /Users/jiangew/.openclaw/.venv
/Users/jiangew/.openclaw/.venv/bin/python -m pip install discord.py
```

## Quality Gate
Validation scripts live in:
- `/Users/jiangew/.openclaw/workspace/validate_outputs.py`
- `/Users/jiangew/.openclaw/workspace/quality_gate.py`
- `/Users/jiangew/.openclaw/workspace/repair_outputs.py`

## Notes
- Ensure agent auth profiles are configured under each agent dir in `/Users/jiangew/.openclaw/agents/`.
- If a provider key is missing, OpenClaw will emit `FailoverError` in gateway logs.
