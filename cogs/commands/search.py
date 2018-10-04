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

class Search:
    def __init__(self, bot):
        self.bot = bot
        self.faceit_data = FaceitData(faceit_token)
    @commands.command()
    async def search(self, ctx, search_term=None, search_value=None):
        search_terms = ["championships", "hubs", "organizers", "players", "teams", "tournaments"]

        if search_term is None:
            await ctx.send("The search term cannot be nothing!")
        elif search_value is None:
            await ctx.send("The search value cannot be nothing!")
        else:
            if search_terms.count(search_term.lower()) == 1:
                if search_term.lower() == "championships":
                    searching = self.faceit_data.search_championships(search_value)
                    if not searching['items']:
                        await ctx.send("No items for that search")
                    else:
                        pass
                        """
                        TODO: Implement search result formatting for all of the search terms.
                        """
                    print(searching)

def setup(bot):
    bot.add_cog(Search(bot))