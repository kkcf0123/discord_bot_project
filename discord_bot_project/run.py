import discord
import os
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
import logging

# discord Token
load_dotenv()
INE_TOKEN = os.getenv('INE_TOKEN')

# intents
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='$', intents = intents)

status = cycle(['멤버들 감시', '쉬고싶어'])

@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} has connected to Discord!')
    await client.load_extension('cogs.cog_manager')
    
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

async def main():
    async with client:
        await client.start(INE_TOKEN)

logging.basicConfig(level=logging.ERROR)
asyncio.run(main())