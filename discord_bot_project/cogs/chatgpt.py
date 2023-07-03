import discord
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class ChatGPTCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.model_name = 'gpt-3.5-turbo'
        self.target_channel_id = None
        self.api_key = os.getenv('CHAT_GPT_API_TOKEN')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('!'): # 만약 커맨드가 실행될 경우
            return

        if message.channel.id == self.target_channel_id:
            input_text = message.content
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            payload = {
                'model': self.model_name,
                'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                             {'role': 'user', 'content': input_text}]
            }
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
            reply = response.json()['choices'][0]['message']['content']
            await message.channel.send(reply)

    @commands.command(name='chatgpt채널')
    async def set_channel(self, ctx, channel_id):
        self.target_channel_id = int(channel_id)
        await ctx.send(f"ChatGPT 전용 채널: {channel_id}")

async def setup(client):
    await client.add_cog(ChatGPTCog(client))