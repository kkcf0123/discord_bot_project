import discord
from discord.ext import commands, tasks
import asyncio

class roleCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mobile_role_id = None
        self.mobile_role = None
        self.mobile_members = set()

    @commands.command()
    async def basic_role(self, ctx, role_id):
        self.mobile_role_id = int(role_id)
        self.mobile_role = ctx.guild.get_role(self.mobile_role_id)
        await ctx.send(f'기본역할 설정 완료: {self.mobile_role.name}')
        
    @commands.command(name='모바일')
    async def handle_mobile_command(self, ctx, action:str, role_id) :
        action = action.lower()
        
        if action == '역할':
            await self.role_mobile(ctx, role_id)
        elif action == '탈출':
            await self.escape_mobile(ctx)
        elif action == '연장':
            await self.extend_mobile(ctx)
        else :
            await ctx.reply('잘못된 동작입니다. 다음 중 하나를 선택해주세요: 역할, 탈출, 연장')
            
    @commands.command()
    async def role_mobile(self, ctx, role_id):
        self.mobile_role_id = int(role_id)
        self.mobile_role = ctx.guild.get_role(self.mobile_role_id)
        await ctx.send(f'모바일 역할 설정 완료: {self.mobile_role.name}')

    @commands.command()
    async def escape_mobile(self, ctx):
        member = ctx.author
        if self.mobile_role in member.roles:
            await member.remove_roles(self.mobile_role)
            await ctx.send(f'{member.name}님의 모바일 역할을 제거했습니다.')
        else:
            await ctx.send(f'{member.name}님은 모바일 역할을 가지고 있지 않습니다.')

    @commands.command()
    async def extend_mobile(self, ctx):
        member = ctx.author
        if self.mobile_role in member.roles:
            await member.remove_roles(self.mobile_role)
            await member.add_roles(self.mobile_role)
            await ctx.send(f'{member.name}님의 모바일 역할을 연장했습니다.')
        else:
            await ctx.send(f'{member.name}님은 모바일 역할을 가지고 있지 않습니다.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.client and member.guild.voice_client is None:
            if after.channel and self.mobile_role in member.roles:
                self.mobile_members.add(member)
                await member.send(f'{member.mention}님이 간을 보는 중입니다!\n `10분`동안 자유를 만끽하실 수 있습니다.\n 만약 연장을 원하시면 `10분 후`에 `!모바일 연장`을 입력해주세요. ')
                await asyncio.sleep(600)
                if member in self.mobile_members:
                    await member.add_roles(self.mobile_role)
                    self.mobile_members.remove(member)
            elif before.channel and self.mobile_role in member.roles:
                if member in self.mobile_members:
                    self.mobile_members.remove(member)
                else:
                    await member.remove_roles(self.mobile_role)

        if not member.client and before.channel and not after.channel:
            if self.mobile_role in member.roles:
                await member.remove_roles(self.mobile_role)

    @tasks.loop(hours=1)
    async def clear_mobile_members(self):
        self.mobile_members.clear()

    @clear_mobile_members.before_loop
    async def before_clear_mobile_members(self):
        await self.client.wait_until_ready()

    def cog_unload(self):
        self.clear_mobile_members.cancel()

async def setup(client):
    await client.add_cog(roleCog(client))