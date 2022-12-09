from __future__ import annotations

import asyncio
import glob
import logging
import os
from typing import Any

import discord
import sentry_sdk
from discord import Intents
from discord.ext.commands import Bot
from tortoise import Tortoise

from chloe.database.database import initialize_db
from chloe.models import Guild


class Chloe(Bot):
    def __init__(self, **kwargs: Any):
        super().__init__(
            **kwargs,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=os.getenv("STATUS"),
            ),
            command_prefix=os.getenv("PREFIX", ";"),
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

        # check for blacklisted prefix.
        blacklist_prefix = ("$", ";")  # pg does not play nice with these prefixes
        if any(p in os.getenv("PREFIX") for p in blacklist_prefix):
            self.logger.fatal("Prefix contains an invalid character")
            exit(0)

        # init database
        await initialize_db()
        self.loop.create_task(self.setup_after())
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

    async def setup_after(self):
        """
        Setup tasks to be performed after connecting to the websocket
        """
        await self.wait_until_ready()
        # update guild table.
        guilds = 0
        for g in self.guilds:
            await Guild.update_or_create(
                guild_id=g.id,
                name=g.name,
                owner_id=g.owner.id,
            )
            guilds += 1
        self.logger.info(f"Updated {guilds} guilds")

    def run(self, **kwargs: Any):
        try:
            super().run(os.getenv("TOKEN", ""), reconnect=True, **kwargs)
        finally:
            self.logger.info("Cleaning up database connections and shutting down")
            close = asyncio.new_event_loop()
            close.run_until_complete(Tortoise.close_connections())
