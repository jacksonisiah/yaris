from __future__ import annotations

import glob
import logging
import os
from typing import Any

import discord
import sentry_sdk
from discord import Intents
from discord.ext.commands import Bot

from chloe.database.database import initialize_db
from chloe.models import Guild


class Chloe(Bot):
    def __init__(self, **kwargs: Any):
        super().__init__(
            **kwargs,
            command_prefix=os.getenv("PREFIX", ";"),
            intents=Intents.all(),
            help_command=None,  # ugliest formatting ever
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
        # init database
        await initialize_db()
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

    async def on_ready(self):
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

    def run(self, **kwargs: Any):
        super().run(os.getenv("TOKEN", ""), reconnect=True, **kwargs)
