from __future__ import annotations

import datetime
import math
from typing import Optional

import dateparser
import discord.ext.commands
import pytz
from discord import app_commands

from chloe.chloe import Chloe
from chloe.models import Reminder as ReminderDb


class Reminder(app_commands.Group):
    @app_commands.command(description="Create a reminder")
    @app_commands.describe(schedule="When you want the alert for this reminder to fire")
    @app_commands.describe(content="The content of the reminder")
    async def create(
        self,
        cmd: discord.Interaction,
        schedule: Optional[str],
        content: str,
    ):
        sch = ""
        time = 0
        # Parse to future date as utc
        if schedule is not None:
            time = dateparser.parse(
                schedule,
                settings={"PREFER_DATES_FROM": "future", "TIMEZONE": "UTC"},
            )
            sch = f" for {schedule}"

        rdb = await ReminderDb.create(
            user=cmd.user.id,
            content=content,
            channel=cmd.channel.id,
            scheduled=time,
        )
        await cmd.response.send_message(f"Reminder #{rdb.id}{sch} saved: `{content}`")

    @app_commands.command(description="List all of your reminders")
    async def list(self, cmd: discord.Interaction):
        rdb = await ReminderDb.filter(user=cmd.user.id).all()
        if len(rdb) == 0:
            return await cmd.response.send_message("You have no reminders.")

        reminder_list = ""
        for r in rdb:
            if r.scheduled > datetime.datetime.now(pytz.UTC):
                ts = math.floor(r.scheduled.timestamp())
                reminder_list += f"#{r.id} (<t:{ts}:R>): `{r.content}`\n"
            elif r.scheduled <= pytz.UTC.localize(
                dt=datetime.datetime(1971, 1, 1, 0, 0, 0),
            ):
                reminder_list += f"#{r.id}: {r.content}\n"

        embed = discord.Embed(
            title="Your Reminders",
            description=f"{reminder_list}",
            color=discord.Color.blue(),
        )
        return await cmd.response.send_message(embed=embed)

    @app_commands.command(description="Delete a reminder")
    @app_commands.describe(reminder_id="The reminder in question's ID")
    async def delete(
        self,
        cmd: discord.Interaction,
        reminder_id: int,
    ):
        rdb = await ReminderDb.get_or_none(id=reminder_id)
        if rdb is not None:
            await rdb.delete()
            return await cmd.response.send_message("Done.")
        else:
            return await cmd.response.send_message("That reminder doesn't exist.")

    # todo: add confirm step modal
    @app_commands.command(description="Clear all reminders")
    async def clear(self, cmd: discord.Interaction):
        reminders = await ReminderDb.filter(user=cmd.user.id).all()
        for r in reminders:
            await r.delete()
        return await cmd.response.send_message("Done.")


async def setup(bot: Chloe):
    bot.tree.add_command(Reminder())
