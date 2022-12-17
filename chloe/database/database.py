from __future__ import annotations

import asyncio
import logging

import tortoise
from dotenv import dotenv_values
from tortoise import Tortoise

_config = dotenv_values(".env")
database_config = {
    "connections": {
        "default": f"postgres://{_config.get('PG_USER')}:{_config.get('PG_PASS')}@{_config.get('PG_HOST')}:"
        f"{_config.get('PG_PORT')}/chloe",
    },
    "apps": {
        "models": {
            "models": ["chloe.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_database():
    """
    Initializes a connection with a PostgresSQL database
    """
    try:
        await Tortoise.init(database_config)
        await Tortoise.generate_schemas()
    except (ConnectionRefusedError, tortoise.ConfigurationError, OSError) as err:
        logger = logging.getLogger("discord")
        logger.critical(f"Could not establish database connection: {err}")
        exit(1)


def cleanup(_signum, _frame):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.close_connections())
