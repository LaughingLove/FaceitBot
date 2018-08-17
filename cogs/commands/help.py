import discord
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        res = (
           ":question: **Help** :question:\n"
            "-----------------------------\n"
            "\n"
            ":question: Help Command\n"
            "Gives you help information\n"
            "*.help*\n"
            "\n"
            ":mag: Player Command\n"
            "Gives you information on a player's stats\n"
            "*.player [faceit-nickname]*\n"
            "\n"
            ":mag: Team Command\n"
            "Gives you information on a team\n"
            "*.team [name-or-url]* -- Use the FACEIT team name or their URL\n"
            "\n"
            ":mag: Team Stats Command\n"
            "Gives you information on a team's stats\n"
            "*.team-stats [name-or-url] [game]* -- Specify a FACEIT team name or URL, and a game (e.g. 'csgo')\n"
            "\n"
        )
        await ctx.author.send(res)

        # Checking if it's a DM channel
        if ctx.guild is not None:
            await ctx.send("Sent you a PM")

def setup(bot):
    bot.add_cog(Help(bot))