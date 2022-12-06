from __future__ import annotations

import glob
import logging
import os
from typing import Any

import discord
import sentry_sdk
from discord import Intents
from discord.ext.commands import Bot


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

    async def setup_hook(self):
        # Load all extensions
        await self.load_extension("jishaku")
        for path in glob.glob("./chloe/extensions/*.py"):
            try:
                name = os.path.basename(os.path.normpath(path)).replace(".py", "")
                await self.load_extension("chloe.extensions." + name)
            except Exception as e:
                self.logger.error(f"Failed loading extension: {e}")

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=os.getenv("STATUS", "Chloe"),
            ),
        )
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

    def run(self, **kwargs: Any):
        super().run(os.getenv("TOKEN", ""), reconnect=True, **kwargs)
