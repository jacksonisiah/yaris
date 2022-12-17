from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class Guild(Model):
    id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField(null=False, unique=True)
    name = fields.CharField(max_length=100)
    prefix = fields.CharField(max_length=10)
    owner_id = fields.BigIntField(null=False)
    active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name
