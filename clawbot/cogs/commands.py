import discord
from discord.ext import commands
from datetime import datetime


def guild_allowed(ctx, allowed_guilds):
    if not allowed_guilds:
        return True
    if ctx.guild is None:
        return False
    return ctx.guild.id in allowed_guilds


def is_admin(ctx, admin_user_ids, admin_role_ids):
    if ctx.author.id in admin_user_ids:
        return True
    if ctx.guild is None:
        return False
    if not admin_role_ids:
        return False
    return any(role.id in admin_role_ids for role in getattr(ctx.author, "roles", []))


def command_allowed(ctx, allowed_guilds, admin_user_ids, admin_role_ids, admin_only_commands, command_name):
    if not guild_allowed(ctx, allowed_guilds):
        return False
    if command_name in admin_only_commands:
        return is_admin(ctx, admin_user_ids, admin_role_ids)
    return True


class CommandCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        allowed_guilds=None,
        admin_user_ids=None,
        admin_role_ids=None,
        admin_only_commands=None,
    ):
        self.bot = bot
        self.allowed_guilds = allowed_guilds or set()
        self.admin_user_ids = admin_user_ids or set()
        self.admin_role_ids = admin_role_ids or set()
        self.admin_only_commands = admin_only_commands or []

    @commands.command()
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def hello(self, ctx):
        if not command_allowed(
            ctx,
            self.allowed_guilds,
            self.admin_user_ids,
            self.admin_role_ids,
            self.admin_only_commands,
            "hello",
        ):
            return
        await ctx.send("Hi，I'm Clawbot 🤖")

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def ping(self, ctx):
        if not command_allowed(
            ctx,
            self.allowed_guilds,
            self.admin_user_ids,
            self.admin_role_ids,
            self.admin_only_commands,
            "ping",
        ):
            return
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def echo(self, ctx, *, message: str):
        if not command_allowed(
            ctx,
            self.allowed_guilds,
            self.admin_user_ids,
            self.admin_role_ids,
            self.admin_only_commands,
            "echo",
        ):
            return
        await ctx.send(message)

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.guild)
    async def stats(self, ctx):
        if not command_allowed(
            ctx,
            self.allowed_guilds,
            self.admin_user_ids,
            self.admin_role_ids,
            self.admin_only_commands,
            "stats",
        ):
            return
        guild = ctx.guild
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        await ctx.send(
            f"Guild: {guild.name} | Members: {guild.member_count} | Time: {now}"
        )

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def reload(self, ctx, cog: str = "all"):
        if not is_admin(ctx, self.admin_user_ids, self.admin_role_ids):
            await ctx.send("权限不足")
            return
        targets = ["cogs.commands", "cogs.listeners"] if cog == "all" else [f"cogs.{cog}"]
        failures = []
        for ext in targets:
            try:
                await self.bot.reload_extension(ext)
            except Exception as exc:
                failures.append(f"{ext}: {exc}")
        if failures:
            await ctx.send("Reload failed:\\n" + "\\n".join(failures))
        else:
            await ctx.send("Reload ok")


async def setup(bot: commands.Bot):
    # allowed_guilds injected via bot.config
    cfg = getattr(bot, "config", {})
    allowed = cfg.get("allowed_guilds", set())
    admin_users = cfg.get("admin_user_ids", set())
    admin_roles = cfg.get("admin_role_ids", set())
    admin_only = cfg.get("admin_only_commands", [])
    await bot.add_cog(
        CommandCog(
            bot,
            allowed_guilds=allowed,
            admin_user_ids=admin_users,
            admin_role_ids=admin_roles,
            admin_only_commands=admin_only,
        )
    )
