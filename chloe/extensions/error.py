from __future__ import annotations

import logging
from typing import Any

import discord
from discord.ext import commands


# noinspection PyBroadException
class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Any):
        # ignore if a custom handler is present
        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)
        ignored = (commands.CommandNotFound, commands.UserInputError)
        invalid_perms = (commands.MissingPermissions, commands.NotOwner)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} is disabled.")
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(
                    "{ctx.command} can only be used in a server.",
                )
            except discord.HTTPException:  # edge case of the century
                self.logger.warning("A guild-only command in DMs was used, but the bot cannot reject it.")
        elif isinstance(error, invalid_perms):
            return await ctx.send("Nope.")

        # something actually went wrong
        await ctx.send("Something went wrong, we have been notified about it.")

        self.logger.error(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
