from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class Reminder(Model):
    id = fields.IntField(pk=True)
    user = fields.IntField()
    content = fields.TextField()

    def __str__(self):
        return self.content
