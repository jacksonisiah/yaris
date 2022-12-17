"""
The following cog is only really useful inside Circle People. I can't support this for personal usage.
If you see something that can be improved, feel free to fix it or get in touch.
"""
from __future__ import annotations

import asyncio
import os
import re
from typing import Any

import discord
from discord.ext import commands

from chloe.chloe import Chloe


class CirclePeople(commands.Cog):
    def __init__(self, bot: Chloe):
        self.bot = bot
        self.SERVER_ID: int = int(os.getenv("SERVER_ID", 0))
        self.SCOREPOST_USER_ID: int = int(os.getenv("SCOREPOST_USER_ID", 0))
        self.SCOREPOST_AUTO_ID: int = int(os.getenv("SCOREPOST_AUTO_ID", 0))
        self.UPLOAD_QUEUE_ID: int = int(os.getenv("UPLOAD_QUEUE_ID", 0))
        self.INFOPEOPLE_ID: int = int(os.getenv("INFOPEOPLE_ID", 0))
        self.UPLOADER_ID: int = int(os.getenv("UPLOADER_ID", 0))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Drop out if not in circle people.
        if message.guild is None or message.guild.id != self.SERVER_ID:
            return
        # Handle user-submission
        if message.channel.id == self.SCOREPOST_USER_ID:
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        # Handle auto-submission
        elif message.channel.id == self.SCOREPOST_AUTO_ID:
            await asyncio.sleep(2)  # wait to clear reactions from score-post-notifier
            await message.clear_reactions()
            await message.add_reaction("✅")  # add reaction

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: Any):
        """
        This is a raw method to avoid an edge case when reacting to a message that came before the bot was started.
        Normal on_reaction_add will completely ignore a message if it is not in the cache.
        """
        if self.SERVER_ID == 0:
            return  # apparently this method will still call even if the cog is not loaded?

        origin = await self.bot.fetch_channel(payload.channel_id)
        queue = await self.bot.fetch_channel(self.UPLOAD_QUEUE_ID)
        if not isinstance(origin, discord.TextChannel):
            return
        elif not isinstance(queue, discord.TextChannel):
            return

        message = await origin.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        if user.bot or message.channel.id != self.SCOREPOST_AUTO_ID:
            return

        # format message
        match = re.search(
            r"https://redd.it/([A-Za-z0-9\-]+)",
            message.content,
            re.IGNORECASE,
        )
        url = match.group(0) if match else "None provided"

        content = re.sub(
            f"<@&{self.INFOPEOPLE_ID}>:",
            "",
            message.content,
            flags=re.IGNORECASE,
        )
        content = re.sub(
            r"https://redd.it/([A-Za-z0-9\-]+).*",
            "",
            content,
            flags=re.IGNORECASE,
        )
        # create embed
        embed = discord.Embed(
            title="New Upload Queue Item",
            description=content,
            color=discord.Color.magenta(),
        )
        embed.add_field(name="Link", value=url)

        await queue.send(f"<@&{self.UPLOADER_ID}>", embed=embed)

    # Helper commands for thumbnail creation.
    @commands.hybrid_command(name="osuava")
    async def osu_avatar(self, ctx: commands.Context, uid: str):
        await ctx.send(f"https://a.ppy.sh/{uid}")

    @commands.hybrid_command(name="osubg")
    async def osu_bg(self, ctx: commands.Context, bgid: str):
        await ctx.send(f"https://assets.ppy.sh/beatmaps/{bgid}/covers/fullsize.jpg")


async def setup(bot: Chloe):
    if os.getenv("SERVER_ID", 0) != 0:
        await bot.add_cog(CirclePeople(bot))
