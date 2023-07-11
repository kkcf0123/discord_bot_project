import discord
import os
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
import logging

# discord Token
load_dotenv()
Token = os.getenv('your_token')

# intents
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='$', intents = intents)

status = cycle(['A', 'B'])

@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} online')
    await client.load_extension('cogs.cog_manager')
    
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

async def main():
    async with client:
        await client.start(Token)

logging.basicConfig(level=logging.ERROR)
asyncio.run(main())
