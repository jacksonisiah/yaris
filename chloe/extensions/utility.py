from __future__ import annotations

import calendar
from typing import Optional

import discord
from discord.ext import commands

from chloe.models import Guild


class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command("help")
    async def help(self, ctx: commands.Context):
        await ctx.send(
            embed=discord.Embed(
                title="Get Help",
                description="[Chloe command reference](https://github.com/jacksonisiah/yaris/wiki/Commands)",
                color=discord.Color.dark_red(),
            ),
        )

    @commands.has_permissions(manage_messages=True)
    @commands.command("cleanup")
    async def cleanup(self, ctx: commands.Context, num: int):
        if isinstance(ctx.channel, discord.TextChannel):
            await ctx.channel.purge(limit=num, check=lambda m: m.author == ctx.author)
            return await ctx.send(f"Cleaned {num} messages.")
        else:
            raise commands.NoPrivateMessage

    @commands.guild_only()
    @commands.hybrid_command("profile")
    async def profile(self, ctx: commands.Context, member: Optional[discord.Member]):
        global status
        member = ctx.author if member is None else member

        if member.nick:
            title = f"{member.nick} ({member.name}#{member.discriminator})"
        else:
            title = f"{member.name}#{member.discriminator}"
        if member.guild_permissions.administrator:
            title += " 🌠"

        if member.activity:
            if member.activity.type == discord.ActivityType.listening:
                status = f"listening to `{member.activity.title}` by `{member.activity.artist}`"
            elif member.activity.type == discord.ActivityType.playing:
                status = f"playing `{member.activity.name}`"
        elif member.status == discord.Status.dnd:
            status = "`do not disturb`"
        else:
            status = f"`{member.status.__str__()}`"

        time: str = (
            calendar.timegm(member.joined_at.utctimetuple()) if not None else "never"
        )

        embed = discord.Embed(
            title=title,
            description=f"Joined <t:{time}:R>\nCurrently {status}\nRole: <@&{member.roles[-1].id}>\n",
            color=member.color,
        )
        embed.add_field(name="Last.fm", value="More to come", inline=False)
        embed.add_field(name="League of Legends", value="More to come", inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(
            text="Does your mom know you have that avatar?",  # todo: easter eggs
            icon_url=self.bot.user.avatar.url,
        )

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.hybrid_command("server")
    async def server(self, ctx: commands.Context):
        guild = ctx.guild
        guild_db = await Guild.filter(guild_id=ctx.guild.id).first()

        embed = discord.Embed(
            title=guild.name,
            description=f"{guild.member_count} members, {len(guild.channels)} channels\n"
            f"Owner: {guild.owner.mention}\n"
            f"{len(guild.roles)} roles\n"
            f"Created <t:{calendar.timegm(guild.created_at.utctimetuple())}:R>\n"
            f"Prefix: `{guild_db.prefix}`",
            color=discord.Color.dark_red(),
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="More to come.", icon_url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utilities(bot))
