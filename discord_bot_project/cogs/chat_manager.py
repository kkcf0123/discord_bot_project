import discord
import json
import asyncio
from discord.ext import commands, tasks

class ChatManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.restricted_data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.load_restricted_data()

    @commands.command(name='채팅제한')
    async def handle_restricted_word(self, ctx, action: str, word=None, channel: discord.TextChannel = None):
        action = action.lower()

        if action == '추가':
            await self.add_restricted_word(ctx, word, channel)
        elif action == '삭제':
            await self.remove_restricted_word(ctx, word, channel)
        elif action == '조회' or action == '목록':
            await self.show_restricted_list(ctx)
        elif action == '초기화':
            await self.initialize_restricted_data(ctx)
        else:
            await ctx.send("`다음 중 하나를 선택해주세요: 추가, 삭제, 조회, 목록, 초기화`")

    async def initialize_restricted_data(self, ctx):
        self.restricted_data = {}
        self.save_restricted_data()
        await ctx.send("허용된 단어 데이터가 초기화되었습니다.")

    async def add_restricted_word(self, ctx, word, channel):
        if word is None:
            await ctx.send("추가할 허용단어를 입력해주세요.")
            return

        word = word.lower()

        if channel:
            if channel.id not in self.restricted_data:
                self.restricted_data[channel.id] = []

            if word in self.restricted_data[channel.id]:
                await ctx.reply(f'`{word}`는 이미 해당 채널에 대해 허용된 단어입니다.')
            else:
                self.restricted_data[channel.id].append(word)
                self.save_restricted_data()
                await ctx.send(f"'{word}'가 채널 '{channel.mention}'에 대해 허용단어로 추가되었습니다.")
        else:
            await ctx.send("채널을 지정해주세요.")

    async def remove_restricted_word(self, ctx, word, channel):
        if word is None:
            await ctx.send("삭제할 단어를 입력해주세요.")
            return

        word = word.lower()

        if channel:
            if channel.id in self.restricted_data and word in self.restricted_data[channel.id]:
                self.restricted_data[channel.id].remove(word)
                self.save_restricted_data()

                # Display current restricted word list
                current_words = self.restricted_data[channel.id]
                word_list = "\n".join(current_words)
                if word_list:
                    await ctx.send(f"현재 {channel.mention} 채널의 허용된 단어 목록:\n{word_list}")
                else:
                    await ctx.send(f"{channel.mention} 채널에 등록된 허용된 단어가 없습니다.")

                await ctx.send(f"'{word}'가 채널 '{channel.mention}'에 대해 혀용된 단어가 삭제 되었습니다.")
            else:
                await ctx.reply(f'`{word}`는 해당 채널에 대해 혀용된 단어가 아닙니다.')
        else:
            await ctx.send("채널을 지정해주세요.")

    async def show_restricted_list(self, ctx):
        if self.restricted_data:
            embed = discord.Embed(title="허용된 채팅 정보", color=discord.Color.blue())
            for channel_id, words in self.restricted_data.items():
                channel = self.client.get_channel(channel_id)
                word_list = "\n".join(words)
                embed.add_field(name=f"채널: {channel.name}", value=word_list, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("등록된 허용단어가 없습니다.")

    def save_restricted_data(self):
        with open("restricted_data.json", "w") as file:
            json.dump(self.restricted_data, file)

    def load_restricted_data(self):
        try:
            with open("restricted_data.json", "r") as file:
                self.restricted_data = json.load(file)
        except FileNotFoundError:
            self.restricted_data = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.restricted_data:
            channel_id = message.channel.id
            if channel_id in self.restricted_data:
                if not message.author.guild_permissions.administrator and not message.author.bot:
                    restricted_words = self.restricted_data[channel_id]
                    if not any(message.content.lower().startswith(word) for word in restricted_words):
                        await message.delete()
                        warning_msg = await message.channel.send("제한된 채팅이 적용 중입니다.커맨드만을 사용 부탁드립니다.")
                        await asyncio.sleep(2)
                        await warning_msg.delete()

async def setup(client):
    await client.add_cog(ChatManager(client))
