import discord
import requests
import asyncio
from discord import Embed
from discord.ext import commands

class TwitchNotifier(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.discord_channel = 'your_discord_text_channel_id'
        self.active_notifiers = {}

    @commands.command(name='뱅')
    async def twitch_command(self, ctx, twitch_account_id):
        twitch_api_url = f"https://api.twitch.tv/helix/streams?user_login={twitch_account_id}"
        headers = {
            'Authorization': 'Bearer your_token',
            'Client-Id': 'your_client_id'
        }

        async def check_streaming_and_notify():
            response = requests.get(twitch_api_url, headers=headers)
            stream_data = response.json()

            if 'data' in stream_data and stream_data['data']:
                stream_info = stream_data['data'][0]

                if twitch_account_id not in self.active_notifiers:
                    self.active_notifiers[twitch_account_id] = stream_info
                    await self.client.get_channel(self.discord_channel).send('Streaming Now!')
            else:
                if twitch_account_id in self.active_notifiers:
                    del self.active_notifiers[twitch_account_id]
                    await self.client.get_channel(self.discord_channel).send("Not Started Streaming.")

        async def loop_check_streaming():
            while True:
                await check_streaming_and_notify()
                await asyncio.sleep(60)

        twitch_notifier = asyncio.create_task(loop_check_streaming())
        await ctx.send(f'Twitch notifier for {twitch_account_id} started!')

async def setup(client):
    await client.add_cog(TwitchNotifier(client))
