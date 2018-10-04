import discord
from discord.ext import commands
import json

from datetime import datetime

from faceit_api.faceit_data import FaceitData

with open('./config_bot.json') as f:
    jsonfile = json.load(f)

faceit_token = jsonfile['faceit-token']

current_time = datetime.now().strftime('%Y-%m-%d %H:%M')


class Player:
    def __init__(self, bot):
        self.bot = bot
        self.faceit_data = FaceitData(faceit_token)

    @commands.command()
    async def player(self, ctx, player=None, game=None):
        if player is None:
            ctx.send("You need to specify a player nickname!")
        else:
            player_info = self.faceit_data.player_details(player)
            # print(player_info)

            faceit_url = player_info['faceit_url'].replace("{lang}", "en")

            embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name=player)
            embed.set_thumbnail(url=player_info['avatar'])

            embed.add_field(
                name="Country",
                value=player_info['country'].upper(),
                inline=True
            )
            embed.add_field(
                name="FACEIT URL",
                value=faceit_url,
                inline=True
            )

            if player_info['games']:
                all_games = list(player_info['games'].keys())

                if game is None:
                    for game_for_player in all_games:
                        if game_for_player == "csgo":
                            game_title = "CS:GO"
                        else:
                            game_title = game_for_player
                        embed.add_field(
                            name="{} ELO".format(game_title),
                            value=player_info['games'][all_games[all_games.index(
                                game_for_player)]]['faceit_elo'],
                            inline=True
                        )
                        embed.add_field(
                            name="{} skill level".format(game_title),
                            value=player_info['games'][all_games[all_games.index(
                                game_for_player)]]['skill_level_label'],
                            inline=True
                        )
                else:
                    embed.add_field(
                        name="{} ELO".format(game.upper()),
                        value=player_info['games'][game]['faceit_elo'],
                        inline=True
                    )
                    embed.add_field(
                        name="{} skill level".format(game.upper()),
                        value=player_info['games'][game]['skill_level_label'],
                        inline=True
                    )

            # infractions = list(player_info['infractions'].keys())

            if player_info['infractions']['last_infraction_date']:
                embed.add_field(
                    name="Last infraction",
                    value=player_info['infractions']['last_infraction_date'],
                    inline=False
                )
                embed.add_field(
                    name="Number of AFKs",
                    value=player_info['infractions']['afk'],
                    inline=True
                )
                embed.add_field(
                    name="Number of leaves in-game",
                    value=player_info['infractions']['leaver'],
                    inline=True
                )

            if len(player_info['bans']) is not 0:
                embed.add_field(
                    name="Bans",
                    value=len(player_info['bans']),
                    inline=True
                )
                embed.add_field(
                    name="Last banned",
                    value="""
                    Ban created at: {} 
                    Ends at: {} 
                    Reason: {}""".format(player_info['bans'][0]['created_at'], player_info['bans'][0]['ends_at'], player_info['bans'][0]['reason']),
                    inline=True
                )
            embed.set_footer(text="Data retrieved at {}".format(current_time))
            await ctx.send(embed=embed)

    @commands.command(aliases=['player-stats', 'playerstats'])
    async def player_stats(self, ctx, name=None, game=None, map=None):
        if name is None:
            await ctx.send("Please specify a FACEIT nickname!")
        else:
            if game is None:
                await ctx.send("Please specify a game on FACEIT")
            else:
                player_info = self.faceit_data.player_details(name)

                player_id = player_info['player_id']

                player_stats = self.faceit_data.player_stats(player_id, game)

                if player_stats is None:
                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name='Error')
                    embed.description = "There was an error retrieving this player's stats, either he has none or the player wasn't found!"
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=discord.Color.green()
                    )
                    embed.set_author(name=player_info['nickname'])
                    embed.set_thumbnail(url=player_info['avatar'])

                    if map is None:
                        embed.description = "{}'s stats".format(
                            player_info['nickname'])

                        embed.add_field(
                            name="Average K/D Ratio",
                            value=player_stats['lifetime']["Average K/D Ratio"],
                            inline=True
                        )
                        embed.add_field(
                            name="Longest Win Streak",
                            value=player_stats['lifetime']['Longest Win Streak'],
                            inline=True
                        )

                        embed.add_field(
                            name="Current Win Streak",
                            value=player_stats['lifetime']['Current Win Streak'],
                            inline=True
                        )

                        embed.add_field(
                            name='Matches Played',
                            value=player_stats['lifetime']['Matches'],
                            inline=True
                        )

                        embed.add_field(
                            name="Win Rate",
                            value="{}%".format(
                                player_stats['lifetime']['Win Rate %']),
                            inline=True
                        )

                        recent_results = []

                        for result in player_stats['lifetime']['Recent Results']:
                            if result == "1":
                                recent_results.append("W")
                            elif result == "0":
                                recent_results.append("L")

                        embed.add_field(
                            name="Recent Match Results",
                            value=' '.join(recent_results),
                            inline=True
                        )

                        embed.add_field(
                            name="Total Wins",
                            value=player_stats['lifetime']['Wins'],
                            inline=True
                        )

                        embed.add_field(
                            name="Average Headshot %",
                            value="{}%".format(
                                player_stats['lifetime']['Average Headshots %']),
                            inline=True
                        )
                        embed.set_footer(text="Data retrieved at {}".format(current_time))
                        await ctx.send(embed=embed)
                    else:
                        found = False
                        counter = 0

                        for segment in player_stats['segments']:
                            if segment['label'] == map:
                                found = True
                                break
                            else:
                                counter += 1

                        map_stats = player_stats['segments'][counter]

                        if found:
                            embed.description = "{}'s stats on {}".format(
                                player_info['nickname'], map)
                            embed.set_thumbnail(url=map_stats["img_small"])

                            embed.add_field(
                                name= "Average K/D Ratio",
                                value= map_stats['stats']['Average K/D Ratio'],
                                inline=True
                            )
                            embed.add_field(
                                name="Average Kills",
                                value = map_stats['stats']['Average Kills'],
                                inline=True
                            )
                            embed.add_field(
                                name="Average Headshot %",
                                value="{}%".format(map_stats['stats']['Average Headshots %']),
                                inline=True
                            )
                            embed.add_field(
                                name="Win Rate",
                                value="{}%".format(map_stats['stats']['Win Rate %']),
                                inline=True
                            )
                            embed.add_field(
                                name="Total Kills",
                                value=map_stats['stats']['Kills'],
                                inline=True
                            )
                            embed.add_field(
                                name="Total Matches",
                                value=map_stats['stats']['Matches'],
                                inline=True
                            )
                            embed.add_field(
                                name="Total Wins",
                                value=map_stats['stats']['Wins'],
                                inline=True
                            )
                            embed.add_field(
                                name="Total Kills",
                                value=map_stats['stats']['Kills'],
                                inline=True
                            )
                            embed.add_field(
                                name="Total Deaths",
                                value=map_stats['stats']['Deaths']
                            )
                            embed.add_field(
                                name="Kills",
                                value="""Total Kills: {}
                                Triple Kills: {}
                                Quadro Kills: {}
                                Penta Kills: {}
                                Total Headshots: {}
                                Headshots per match: {}""".format(map_stats['stats']['Kills'], map_stats['stats']['Triple Kills'], map_stats['stats']['Quadro Kills'], map_stats['stats']['Penta Kills'], map_stats['stats']['Headshots'], map_stats['stats']['Headshots per Match'])
                            )
                            embed.set_footer(text="Data retrieved at {}".format(current_time))
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("Couldn't find the map, are you sure said the map correctly (e.g. de_cache)?")


def setup(bot):
    bot.add_cog(Player(bot))
