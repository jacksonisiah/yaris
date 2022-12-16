from __future__ import annotations

import logging
import math

from dateutil import parser
from discord.ext import commands
from discord.ext import tasks

from chloe.models import Reminder


class RemindersTask(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord")
        self.post_reminders.start()

    @tasks.loop(seconds=5)
    async def post_reminders(self):
        """
        Sends out reminders every 5 seconds.
        """
        reminders: list[dict] = await Reminder.get_reminders_now()
        if len(reminders) > 0:
            for r in reminders:
                chan = self.bot.get_channel(r.get("channel"))
                ts = math.floor(r.get("created").timestamp())
                await chan.send(f"<@{r.get('user')}> (<t:{ts}:R>) {r.get('content')}")

    @post_reminders.before_loop
    async def before_setup(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(RemindersTask(bot))
