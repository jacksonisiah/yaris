from __future__ import annotations

from tortoise import connections
from tortoise import fields
from tortoise.models import Model


class Reminder(Model):
    id = fields.IntField(pk=True)
    user = fields.BigIntField()
    content = fields.TextField()
    channel = fields.BigIntField()
    created = fields.DatetimeField(auto_now=True)
    scheduled = fields.DatetimeField()
    snooze_cnt = fields.IntField(default=0)

    def __str__(self):
        return self.content

    @staticmethod
    async def get_reminders_now():
        conn = connections.get("default")
        return await conn.execute_query_dict(
            "select * from reminder where scheduled between now() and now() + interval '5 seconds';",
        )
