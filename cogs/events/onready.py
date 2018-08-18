import discord
from discord.ext import commands

class OnReady:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_ready(self):
        print("{} is now online".format(self.bot.user.name))
        await self.bot.change_presence(activity=discord.Game("Use .help to get started"))

def setup(bot):
    bot.add_cog(OnReady(bot))