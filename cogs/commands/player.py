import discord
from discord.ext import commands
import json

from faceit_api.faceit_data import FaceitData

with open('./config_bot.json') as f:
    jsonfile = json.load(f)

faceit_token = jsonfile['faceit-token']

class Player:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def player(self, ctx, player=None, game=None):
        if player is None:
            ctx.send("You need to specify a player nickname!")
        else:
            faceit_data = FaceitData(faceit_token)

            player_info = faceit_data.player_details(player)
            # print(player_info)

            faceit_url = player_info['faceit_url'].replace("{lang}", "en")

            embed = discord.Embed(
                color = discord.Color.blue()
            )
            embed.set_author(name=player)
            embed.set_thumbnail(url=player_info['avatar'])

            embed.add_field(
                name = "Country",
                value = player_info['country'].upper(),
                inline=True
            )
            embed.add_field(
                name = "FACEIT URL",
                value = faceit_url,
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
                            name = "{} ELO".format(game_title),
                            value = player_info['games'][all_games[all_games.index(game_for_player)]]['faceit_elo'],
                            inline=True
                        )
                        embed.add_field(
                            name = "{} skill level".format(game_title),
                            value = player_info['games'][all_games[all_games.index(game_for_player)]]['skill_level_label'],
                            inline = True
                        )
                else:
                    embed.add_field(
                        name = "{} ELO".format(game.upper()),
                        value = player_info['games'][game]['faceit_elo'],
                        inline = True
                    )
                    embed.add_field(
                        name = "{} skill level".format(game.upper()),
                        value = player_info['games'][game]['skill_level_label'],
                        inline = True
                    )
            
            # infractions = list(player_info['infractions'].keys())

            if player_info['infractions']['last_infraction_date']:
                embed.add_field(
                    name = "Last infraction",
                    value = player_info['infractions']['last_infraction_date'],
                    inline = False
                )
                embed.add_field(
                    name = "Number of AFKs",
                    value = player_info['infractions']['afk'],
                    inline = True
                )
                embed.add_field(
                    name = "Number of leaves in-game",
                    value = player_info['infractions']['leaver'],
                    inline = True
                )
            
            if len(player_info['bans']) is not 0:
                embed.add_field(
                    name = "Bans",
                    value = len(player_info['bans']),
                    inline= True
                )
                embed.add_field(
                    name = "Last banned",
                    value = """
                    Ban created at: {} 
                    Ends at: {} 
                    Reason: {}""".format(player_info['bans'][0]['created_at'], player_info['bans'][0]['ends_at'], player_info['bans'][0]['reason']),
                    inline = True
                )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Player(bot))
