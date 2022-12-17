from __future__ import annotations

import discord
from discord.ext import commands

from chloe.chloe import Chloe


# noinspection PyBroadException
class Error(commands.Cog):
    def __init__(self, bot: Chloe):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, e: commands.CommandError):
        # ignore if a custom handler is present
        if hasattr(ctx.command, "on_error"):
            return

        e = getattr(e, "original", e)
        ignored = (commands.CommandNotFound, commands.UserInputError)
        invalid_perms = (
            commands.MissingPermissions,
            commands.NotOwner,
            commands.CheckFailure,
        )

        if isinstance(e, ignored):
            return
        elif isinstance(e, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} is disabled.")
        elif isinstance(e, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(
                    f"{ctx.command} can only be used in a server.",
                )
            except discord.HTTPException:  # edge case of the century
                self.bot.logger.warning(
                    "A guild-only command in DMs was used, but the bot cannot reject it.",
                )
        elif isinstance(e, invalid_perms):
            return await ctx.send("Nope.")

        # something actually went wrong
        self.bot.logger.error(e, exc_info=True)
        await ctx.send("You broke something, and it has been reported.")


async def setup(bot: Chloe):
    await bot.add_cog(Error(bot))
