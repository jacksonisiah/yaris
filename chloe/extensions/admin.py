from __future__ import annotations

import discord
from discord.ext import commands

from chloe.chloe import Chloe


class Administration(commands.Cog):
    def __init__(self, bot: Chloe) -> None:
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

    @commands.is_owner()
    @commands.command(name="forceleave", hidden=True)
    async def force_leave(self, ctx: commands.Context, guild_id: int = None):
        guild_id = ctx.guild.id if guild_id is None else guild_id
        try:
            guild = await self.bot.fetch_guild(guild_id)
            await guild.leave()
            self.bot.logger.info(f"Force left guild: {ctx.guild.name}")
        except discord.HTTPException as e:
            self.bot.logger.error(f"Leaving guild failed: {e}")
            await ctx.send("Nope.")


async def setup(bot: Chloe):
    await bot.add_cog(Administration(bot))
