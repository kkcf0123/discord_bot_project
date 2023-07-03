import discord
import requests
import asyncio
from discord import Embed
from discord.ext import commands

class TwitchNotifier:
    def __init__(self, client, twitch_account_id):
        self.client = client
        self.twitch_api_url = f"https://api.twitch.tv/helix/streams?user_login={twitch_account_id}"
        self.headers = {
            'Authorization': 'Bearer <your_author>',
            'Client-Id': 'your client id'
        }
        self._stream_data = {}

    async def check_streaming_and_notify(self):
        response = requests.get(self.twitch_api_url, headers=self.headers)
        stream_data = response.json()

        if 'data' in stream_data and stream_data['data']:
            if self._stream_data != stream_data['data'][0]:
                self._stream_data = stream_data['data'][0]

                streamer_name = self._stream_data['user_name']
                stream_title = self._stream_data['title']
                stream_url = 'https://www.twitch.tv/' + streamer_name
                embed = Embed(title=stream_title, url=stream_url)
                embed.set_author(name=streamer_name)
                await self.client.get_channel(950940240783216660).send('스트리밍이 시작되었습니다!', embed=embed)
        else:
            await self.client.get_channel(950940240783216660).send("현재 스트리밍 중이 아닙니다.")

    async def loop_check_streaming(self):
        while True:
            await self.check_streaming_and_notify()
            await asyncio.sleep(60)  # 60초 간격으로 스트리밍 정보를 확인

class TwitchNotifierCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_notifiers = {}

    @commands.command(name='뱅')
    async def twitch_command(self, ctx, twitch_account_id):
        twitch_notifier = TwitchNotifier(self.bot, twitch_account_id)
        await self.add_notifier(twitch_account_id, twitch_notifier)
        await ctx.send(f'Twitch notifier for {twitch_account_id} started!')

    async def add_notifier(self, twitch_account_id, twitch_notifier):
        task = asyncio.create_task(twitch_notifier.loop_check_streaming())
        self.active_notifiers[twitch_account_id] = (twitch_notifier, task)

async def setup(bot):
    await bot.add_cog(TwitchNotifierCog(bot))
