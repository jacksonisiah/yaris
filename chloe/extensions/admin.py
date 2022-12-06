from __future__ import annotations

from discord.ext import commands


class Administration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="sync", hidden=True)
    async def sync_commands(self, ctx: commands.Context):
        resp = await self.bot.tree.sync()
        await ctx.send(f"Syncing slash commands. {len(resp)}")

    @commands.is_owner()
    @commands.command(name="selfnick", hidden=True)
    async def self_nick(self, ctx: commands.Context, *, arg: str):
        await ctx.guild.me.edit(nick=arg)


async def setup(bot: commands.Bot):
    await bot.add_cog(Administration(bot))
