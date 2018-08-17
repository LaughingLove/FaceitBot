import discord
from discord.ext import commands

import json

with open('./config_bot.json') as f:
    tokenfile = json.load(f)

TOKEN = tokenfile['discord-token']

description = "A bot that uses FACEIT's API to give you some stats"

bot = commands.Bot(command_prefix=".", description=description)
bot.remove_command("help")

def format_cog(cogs_dir):
    import os
    found_cogs = []
    formatted_cogs = []
    for path, dirs, files in os.walk("cogs"):
        for f in files:
            if f.endswith(".py"):
                found_cogs.append(os.path.join(path, f))
    for extension in found_cogs:
        newextension = extension.replace(".py", "")
        newextension = newextension.replace("\\", ".")
        formatted_cogs.append(newextension)
    return formatted_cogs

if __name__ == "__main__":
    import traceback
    cogs_dir = "cogs"
    
    for cog in format_cog(cogs_dir):
        try:
            bot.load_extension(cog)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {cog}.')
            traceback.print_exc()
bot.run(TOKEN)