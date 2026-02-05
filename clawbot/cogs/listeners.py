import discord
from discord.ext import commands


class ListenerCog(commands.Cog):
    def __init__(self, bot: commands.Bot, keywords=None, enable_reactions=True):
        self.bot = bot
        self.keywords = [k.lower() for k in (keywords or [])]
        self.enable_reactions = enable_reactions

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.enable_reactions:
            content = message.content.lower()
            if any(k in content for k in self.keywords):
                await message.add_reaction("👀")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Cooldown: {error.retry_after:.1f}s")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("参数缺失，使用 !help 查看用法")
            return
        # fall through: log in main


async def setup(bot: commands.Bot):
    cfg = getattr(bot, "config", {})
    await bot.add_cog(
        ListenerCog(
            bot,
            keywords=cfg.get("keywords", []),
            enable_reactions=cfg.get("enable_reactions", True),
        )
    )
