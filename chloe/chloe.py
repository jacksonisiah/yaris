from __future__ import annotations

import asyncio
import glob
import logging
import os
import signal
import sys
from typing import Any

import discord
import sentry_sdk
from discord import Intents
from discord.ext.commands import Bot

from chloe.database.database import cleanup
from chloe.database.database import init_database
from chloe.models import Guild


class Chloe(Bot):
    def __init__(self, **kwargs: Any):
        super().__init__(
            **kwargs,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=os.getenv("STATUS"),
            ),
            command_prefix=os.getenv("PREFIX", "."),
            intents=Intents.all(),
            help_command=None,
        )
        self.logger = logging.getLogger("discord")
        self.sentry = sentry_sdk.init(os.getenv("SENTRY_DSN"))

    @classmethod
    async def on_guild_join(cls, guild: discord.Guild):
        await Guild.create(
            guild_id=guild.id,
            name=guild.name,
            owner_id=guild.owner.id,
            prefix=os.getenv("PREFIX", "."),
        )

    @classmethod
    async def on_guild_remove(cls, guild: discord.Guild):
        await Guild.filter(guild_id=guild.id).update(active=False)

    @classmethod
    async def on_guild_update(cls, before: discord.Guild, after: discord.Guild):
        await Guild.filter(guild_id=before.id).update(
            name=after.name,
            owner_id=after.owner.id,
        )

    async def setup_hook(self):
        # startup graphic
        self.logger.info(
            """
                   _     _
               ___| |__ | | ___   ___
              / __| '_ \\| |/ _ \\ / _ \\
             | (__| | | | | (_) |  __/
              \\___|_| |_|_|\\___/ \\___|
            \n(c) 2019-2022 Jackson Isaiah, under the ISC license.
            """,
        )

        await init_database()
        self.loop.create_task(self.after_connect())

        # Load all extensions
        await self.load_extension("jishaku")
        for pkg in ("tasks", "extensions"):
            for mod in glob.glob(f"./chloe/{pkg}/*.py"):
                try:
                    name = os.path.basename(os.path.normpath(mod)).replace(".py", "")
                    await self.load_extension(f"chloe.{pkg}.{name}")
                    self.logger.info(f"Successfully initialized extension {name}")
                except Exception as e:
                    self.logger.error(e, exc_info=True)

    async def after_connect(self):
        """
        Setup tasks to be performed after connecting to the websocket
        """
        await self.wait_until_ready()

        # Postgres does not play nice with these prefixes
        blacklist_prefix = ("$", ";")
        if any(p in os.getenv("PREFIX") for p in blacklist_prefix):
            self.logger.fatal("Prefix contains an invalid character")
            exit(0)

        # Populate guild table
        # todo: repository?
        guilds = 0
        for g in self.guilds:
            c = await Guild.get_or_none(guild_id=g.id)
            if c is None:
                await Guild.create(
                    guild_id=g.id,
                    name=g.name,
                    prefix=os.getenv("PREFIX"),
                    owner_id=g.owner.id,
                )
            guilds += 1
        self.logger.info(f"Updated {guilds} guilds")

    def run(self, **kwargs: Any):
        # https://github.com/encode/httpx/issues/914#issuecomment-622586610
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        signal.signal(signal.SIGTERM, cleanup)
        super().run(os.getenv("TOKEN", ""), reconnect=True, **kwargs)
