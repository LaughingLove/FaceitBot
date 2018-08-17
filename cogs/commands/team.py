import discord
from discord.ext import commands

import json

from urllib.parse import urlparse

from faceit_api.faceit_data import FaceitData

with open('./config_bot.json') as f:
    jsonfile = json.load(f)
faceit_token = jsonfile['faceit-token']


class Team:
    def __init__(self, bot):
        self.bot = bot
        self.faceit_data = FaceitData(faceit_token)

    @commands.command()
    async def team(self, ctx, name_or_url=None):
        if name_or_url is None:
            ctx.send("Please specify a name or URL")
        else:
            if not urlparse(name_or_url).scheme:
                search_results = self.faceit_data.search_teams(name_or_url)
                team = self.faceit_data.team_details(
                    search_results['items'][0]['team_id'])
            elif not urlparse(name_or_url).netloc:
                search_results = self.faceit_data.search_teams(name_or_url)
                team = self.faceit_data.team_details(
                    search_results['items'][0]['team_id'])
            else:
                split_url = name_or_url.split("teams/")
                split_url = split_url[1]

                team = self.faceit_data.team_details(split_url)
            
            embed = discord.Embed(
                color=discord.Color.orange()
            )
            embed.set_author(name=team['name'])
            embed.set_thumbnail(url=team['avatar'])

            embed.add_field(
                name="Type of game",
                value=team['game'],
                inline=True
            )
            embed.add_field(
                name="Type of team",
                value=team['team_type'],
                inline=True
            )

            members = list(team['members'])

            for member in members:
                embed.add_field(
                    name="Member",
                    value="{} ({})".format(member['nickname'], member['country']),
                    inline=True
                )
            faceit_url = team['faceit_url'].replace("{lang}", "en")
            embed.add_field(
                name = "FACEIT URL",
                value=faceit_url,
                inline=False
            )

            embed.add_field(
                name="Stats",
                value="Use .team-stats {} [game] to get {}'s team stats".format(
                    team['name'], team['name']),
                inline=False
            )

            await ctx.send(embed=embed)

    @commands.command(aliases=['teamstats', 'team-stats'])
    async def team_stats(self, ctx, name_or_url=None, game=None):
        if name_or_url is None:
            await ctx.send("Please specify a name or URL")
        else:
            if game is None:
                await ctx.send("Please specify a game")
            else:
                if game == "CS:GO":
                    game = "csgo"
                if not urlparse(name_or_url).scheme:
                    search_results = self.faceit_data.search_teams(name_or_url)
                    team = self.faceit_data.team_stats(search_results['items'][0]['team_id'], game)
                elif not urlparse(name_or_url).netloc:
                    search_results = self.faceit_data.search_teams(name_or_url)
                    team = self.faceit_data.team_stats(
                        search_results['items'][0]['team_id'], game)
                else:
                    split_url = name_or_url.split("teams/")
                    split_url = split_url[1]

                    team = self.faceit_data.team_stats(split_url, game)

                if team is None:
                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name="Error loading stats")
                    embed.description = "Either this team has no stats or we couldn't find the team."

                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=discord.Color.dark_orange()
                    )

                    team_name = self.faceit_data.team_details(team['team_id'])

                    embed.set_author(name=team_name['name'])

                    embed.add_field(
                        name="Current Win Streak",
                        value=team['lifetime']['Current Win Streak'],
                        inline=True
                    )
                    embed.add_field(
                        name="Longest Win Streak",
                        value=team['lifetime']['Longest Win Streak'],
                        inline=True
                    )
                    embed.add_field(
                        name="Total number of matches",
                        value=team['lifetime']['Matches'],
                        inline=True
                    )

                    recent_results = []

                    for result in team['lifetime']["Recent Results"]:
                        if result == "1":
                            recent_results.append("W")
                        elif result == "0":
                            recent_results.append("L")

                    embed.add_field(
                        name = "Win ratio",
                        value = "{}%".format(team['lifetime']['Win Rate %']),
                        inline=True
                    )

                    embed.add_field(
                        name="Recent results",
                        value= ' '.join(recent_results),
                        inline=True
                    )

                    embed.add_field(
                        name="Team K/D ratio",
                        value= team['lifetime']['Team Average K/D Ratio'],
                        inline=True
                    )

                    for segment in team['segments']:
                        embed.add_field(
                            name = segment['label'],
                            value="""
                            Matches: {}
                            Win rate: {}%
                            Wins: {}
                            """.format(segment['stats']['Matches'], segment['stats']['Win Rate %'], segment['stats']['Wins']),
                            inline=False
                        )


                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Team(bot))
