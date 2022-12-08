from __future__ import annotations

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guild" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL,
    "prefix" VARCHAR(10) NOT NULL  DEFAULT ';;',
    "owner_id" BIGINT NOT NULL,
    "active" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "reminder" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user" INT NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
