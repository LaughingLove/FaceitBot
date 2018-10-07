import discord
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, category=None):
        embed = discord.Embed(
            color=discord.Color.purple()
        )
        embed.title = ":question: Help :question:"
        
        if category is None:
            embed.add_field(
                name=":exclamation: Info",
                value="Gives you info about the bot. *.info*",
                inline=False
            )
            embed.add_field(
                name=":arrow_up: Levels",
                value="Gives you an ELO to level table! *.levels*"
            )
            embed.add_field(
                name=":mag: Player Category",
                value="Gives you info and stats on a player! Use .help player for more info.",
                inline=False
            )
            embed.add_field(
                name=":mag: Team Category",
                value="Gives you info and stats on a FACEIT team! Use .help team for more info.",
                inline=False
            )
        elif category.lower() == "player":
            embed.add_field(
                name="Player Command",
                value="""Gives you info on a player!
                Use *.player [faceit-nickname]*
                """
            )
            embed.add_field(
                name="Player Stats Command",
                value="""Gives you stats on a player!
                Use *.player-stats [faceit-nickname] [game] <map>*
                """
            )
        elif category.lower() == "team":
            embed.add_field(
                name="Team Command",
                value="""Gives you info on a team!
                Use *.team [team name or URL to team]*
                """
            )
            embed.add_field(
                name="Team Stats Command",
                value="""Gives you stats on a team!
                Use *.team-stats [team name or URL to team] [game] <map>*
                """
            )
        await ctx.author.send(embed=embed)

        # Checking if it's a DM channel
        if ctx.guild is not None:
            await ctx.send("Sent you a PM")

    @commands.command()
    async def info(self, ctx):
        user = self.bot.get_user(127638450437488651)
        await ctx.send("This bot was written by {} using discord.py and the Faceit API. If you have any questions please message add me on discord.".format(user.mention))

def setup(bot):

    bot.add_cog(Help(bot))