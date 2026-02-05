import os
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands


def _validate_config(data: dict):
    if not isinstance(data.get("discord_token", ""), str) or not data["discord_token"]:
        raise ValueError("config: discord_token must be a non-empty string")
    if not isinstance(data.get("bot_prefix", ""), str) or not data["bot_prefix"]:
        raise ValueError("config: bot_prefix must be a non-empty string")
    if not isinstance(data.get("allowed_guilds", []), (list, set)):
        raise ValueError("config: allowed_guilds must be a list of guild IDs")
    if not isinstance(data.get("keywords", []), list):
        raise ValueError("config: keywords must be a list")
    if not isinstance(data.get("enable_reactions", True), bool):
        raise ValueError("config: enable_reactions must be a boolean")
    if not isinstance(data.get("log_level", ""), str):
        raise ValueError("config: log_level must be a string")
    if not isinstance(data.get("admin_user_ids", []), (list, set)):
        raise ValueError("config: admin_user_ids must be a list of user IDs")
    if not isinstance(data.get("admin_role_ids", []), (list, set)):
        raise ValueError("config: admin_role_ids must be a list of role IDs")
    if not isinstance(data.get("admin_only_commands", []), list):
        raise ValueError("config: admin_only_commands must be a list of command names")


def load_config():
    base_path = Path(__file__).resolve().parent
    root_path = base_path.parent
    cfg_path = root_path / "clawbot.config.json"
    local_path = root_path / "clawbot.config.local.json"
    data = {}
    if cfg_path.exists():
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    if local_path.exists():
        local = json.loads(local_path.read_text(encoding="utf-8"))
        data.update(local)

    # Defaults
    data.setdefault("discord_token", "")
    data.setdefault("bot_prefix", "!")
    data.setdefault("allowed_guilds", [])
    data.setdefault("keywords", ["crypto", "btc", "eth", "stablecoin", "polymarket"])
    data.setdefault("enable_reactions", True)
    data.setdefault("log_level", "INFO")
    data.setdefault("admin_user_ids", [])
    data.setdefault("admin_role_ids", [])
    data.setdefault("admin_only_commands", [])

    # Normalize
    data["allowed_guilds"] = set(int(x) for x in data.get("allowed_guilds", []) if str(x).isdigit())
    data["admin_user_ids"] = set(int(x) for x in data.get("admin_user_ids", []) if str(x).isdigit())
    data["admin_role_ids"] = set(int(x) for x in data.get("admin_role_ids", []) if str(x).isdigit())
    data["admin_only_commands"] = [str(x) for x in data.get("admin_only_commands", []) if str(x)]
    _validate_config(data)
    return data


# 1. 设置机器人意图 (Intents)
# 必须与你在 Developer Portal 中开启的权限一致
intents = discord.Intents.default()
intents.message_content = True  # 允许机器人读取消息内容

# 2. 加载配置
config = load_config()

# 3. 日志
logging.basicConfig(
    level=config["log_level"],
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("clawbot")

class ClawBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.commands")
        await self.load_extension("cogs.listeners")


# 4. 创建机器人实例
bot = ClawBot(
    command_prefix=config["bot_prefix"],
    intents=intents,
    help_command=commands.DefaultHelpCommand(),
)

# Attach config for cogs
bot.config = config


@bot.event
async def on_ready():
    logger.info("Logged in as %s (ID: %s, Prefix: %s)", bot.user.name, bot.user.id, config["bot_prefix"])
    logger.info("OpenClaw Discord Bot is now active and monitoring the channels. 🚀")

@bot.event
async def on_command_error(ctx, error):
    # Allow listener cog to handle known errors first
    if isinstance(error, (commands.CommandOnCooldown, commands.MissingRequiredArgument)):
        return
    logger.exception("Command error: %s", error)
    await ctx.send("执行出错，请稍后再试")


def main():
    TOKEN = config.get("discord_token", "")
    if not TOKEN:
        raise RuntimeError("Missing discord_token in config.json/config.local.json")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
