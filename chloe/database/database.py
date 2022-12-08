from __future__ import annotations

import logging

import tortoise
from dotenv import dotenv_values
from tortoise import Tortoise

config = dotenv_values(".env")

database_config = {
    "connections": {"default": config.get("DB_CONNECTION")},
    "apps": {
        "models": {
            "models": ["chloe.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def initialize_db():
    """
    Initializes a connection with a PostgresSQL database
    """
    try:
        await Tortoise.init(database_config)
    except tortoise.ConfigurationError as e:
        logger = logging.getLogger("discord")
        logger.critical(f"Could not establish database connection: {e}")
        exit(1)
