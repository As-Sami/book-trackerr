import discord
import os
from pathlib import Path
from os import environ
from discord.ext.commands import Bot

# CONSTANTS
token = environ.get('BOT_TOKEN')
db_url = environ.get('DATABASE_URL')

# SUPER_USERS=[759026765976567810]

bot = Bot(description='Book---TrackeR' , command_prefix='>', help_command=None)

@bot.event
async def on_ready():
    print('I am ready')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except:
            print(f'Failed to load file {filename}')

bot.run(token)
