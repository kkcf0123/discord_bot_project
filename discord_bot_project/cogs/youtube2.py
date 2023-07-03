import discord
import os
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from dotenv import load_dotenv
from itertools import chain
import json

class YouTubeNotification(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.discord_channel_id = None  # 디스코드 채널 ID를 저장할 변수
        self.youtube_channel_ids = []  # 등록된 YouTube 채널 ID를 저장할 리스트

        load_dotenv()  # .env 파일에서 환경 변수 로드
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')  # .env 파일에서 YouTube API 키 가져오기
        self.youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)

        self.prev_video_ids = {}  # 채널별 이전 비디오 ID를 저장할 딕셔너리
        self.prev_messages = {}  # 채널별 이전 메시지를 저장할 딕셔너리

        self.send_latest_video.start()

    @tasks.loop(hours=1)
    async def send_latest_video(self):
        for channel_id in self.youtube_channel_ids:
            # 최근 비디오 검색
            video_request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=1,
                order="date",
                type="video"
            )
            video_response = video_request.execute()
            if 'items' not in video_response:
                continue

            video_title = video_response['items'][0]['snippet']['title']
            video_id = video_response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail_url = video_response['items'][0]['snippet']['thumbnails']['high']['url']
            
            # 채널 정보 검색
            channel_request = self.youtube.channels().list(
                part="snippet",
                id=channel_id
            )
            channel_response = channel_request.execute()
            channel_name = channel_response['items'][0]['snippet']['title']

            # 새 메시지 전송
            if channel_id not in self.prev_video_ids:
                self.prev_video_ids[channel_id] = video_id
            elif video_id == self.prev_video_ids[channel_id]:
                continue

            discord_channel = self.client.get_channel(self.discord_channel_id)

            if channel_id in self.prev_messages:
                await self.prev_messages[channel_id].delete()

            embed = discord.Embed(title=video_title, url=video_url)
            embed.set_image(url=thumbnail_url)
            embed.set_author(name=channel_name)

            self.prev_messages[channel_id] = await discord_channel.send(embed=embed)
            self.prev_video_ids[channel_id] = video_id
            print(f"새로운 영상 도착~: {video_title}")

    @send_latest_video.before_loop
    async def before_send_latest_video(self):
        await self.client.wait_until_ready()
    
    @commands.command(name='유튜브')
    async def handle_youtube_notify(self, ctx, action, discord_channel_id = None, youtube_channel_id = None):
        action = action.lower()
        
        if action == '알림':
            await self.set_discord_channel(ctx, discord_channel_id)
        elif action == '등록':
            await self.add_youtube_channel(ctx, youtube_channel_id)
        elif action == '삭제':
            await self.remove_youtube_channel(ctx, youtube_channel_id)
        elif action == '조회' or '리스트':
            await self.list_youtube_channels(ctx)
        else :
            await ctx.reply('알림, 등록, 삭제, 조회 or 리스트를 입력해주세요.')
        
    @commands.command(name='유튜브알림')
    async def set_discord_channel(self, ctx, discord_channel_id):
        self.discord_channel_id = int(discord_channel_id)  # 입력한 Discord 채널 ID를 저장
        await ctx.send(f"유튜브 알림을 {discord_channel_id}로 설정했습니다.")

    @commands.command(name='유튜브등록')
    async def add_youtube_channel(self, ctx, youtube_channel_id):
        if youtube_channel_id not in self.youtube_channel_ids:
            self.youtube_channel_ids.append(youtube_channel_id)
            await ctx.send(f"YouTube 채널 {youtube_channel_id}를 등록했습니다.")
        else:
            await ctx.send(f"YouTube 채널 {youtube_channel_id}는 이미 등록되어 있습니다.")

    @commands.command(name='유튜브삭제')
    async def remove_youtube_channel(self, ctx, youtube_channel_id):
        if youtube_channel_id in self.youtube_channel_ids:
            self.youtube_channel_ids.remove(youtube_channel_id)
            await ctx.send(f"YouTube 채널 {youtube_channel_id}를 삭제했습니다.")
        else:
            await ctx.send(f"YouTube 채널 {youtube_channel_id}는 등록되어 있지 않습니다.")

    @commands.command(name='유튜브리스트')
    async def list_youtube_channels(self, ctx):
        embed = discord.Embed(title="등록된 YouTube 채널 리스트")
        if self.youtube_channel_ids:
            for channel_id in self.youtube_channel_ids:
                embed.add_field(name="YouTube 채널 ID", value=channel_id, inline=False)
        else:
            embed.description = "등록된 YouTube 채널이 없습니다."
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(YouTubeNotification(client))
