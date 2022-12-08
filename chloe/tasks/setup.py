from __future__ import annotations

import logging
import os

import discord
from discord.ext import commands
from discord.ext import tasks

from chloe.models import Guild


class SetupTask(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.presence: str = os.getenv("STATUS")
        self.logger = logging.getLogger("discord")
        self.setup_ready.start()

    @tasks.loop(seconds=0, count=1)
    async def setup_ready(self):
        # add or update all guilds to database
        guilds = 0
        for g in self.bot.guilds:
            await Guild.update_or_create(
                guild_id=g.id,
                name=g.name,
                owner_id=g.owner.id,
            )
            guilds += 1
        self.logger.info(f"Updated {guilds} guilds")

        # set presence
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=self.presence,
            ),
        )

    @setup_ready.before_loop
    async def before_setup(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(SetupTask(bot))
