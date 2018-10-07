import discord
from discord.ext import commands

import json

from datetime import datetime

from urllib.parse import urlparse

from faceit_api.faceit_data import FaceitData

with open('./config_bot.json') as f:
    jsonfile = json.load(f)
faceit_token = jsonfile['faceit-token']

current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

class Levels:
    def __init__(self, bot):
        self.bot = bot
        self.faceit_data = FaceitData(faceit_token)

    @commands.command(aliases=['elolevels'])
    async def levels(self, ctx):
        embed = discord.Embed(
            color=discord.Color.dark_magenta()
        )
        embed.set_author(name="ELO Levels")
        embed.add_field(
            name="1",
            value="1-800 ELO"
        )
        embed.add_field(
            name="2",
            value="801-950 ELO"
        )
        embed.add_field(
            name="3",
            value="951-1100 ELO"
        )
        embed.add_field(
            name="4",
            value="1101-1250 ELO"
        )
        embed.add_field(
            name="5",
            value="1251-1400 ELO"
        )
        embed.add_field(
            name="6",
            value="1401-1550 ELO"
        )
        embed.add_field(
            name="7",
            value="1551-1700"
        )
        embed.add_field(
            name="8",
            value="1701-1850 ELO"
        )
        embed.add_field(
            name="9",
            value="1851-2000 ELO"
        )
        embed.add_field(
            name="10",
            value="2001+ ELO"
        )
        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(Levels(bot))