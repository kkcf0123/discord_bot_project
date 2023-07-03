import discord
import asyncio
import os
from discord import Embed
from discord.ext import commands

class CogManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name='코그리스트')
    async def check_cogs(self, ctx):
        if ctx.author.guild_permissions.administrator:
            loaded_cogs = list(self.client.extensions.keys())
            cogs_without_prefix = [cog.replace("cogs.", "") for cog in loaded_cogs]
            
            embed = Embed(title="확인된 Cogs", description=", ".join(cogs_without_prefix), color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.")
            
    @commands.command(name='코그로드')
    async def load(self, ctx, *, cog: str):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.client.load_extension(f"cogs.{cog}")
            except commands.ExtensionAlreadyLoaded:
                return await ctx.send(f"{cog} 가 이미 로드되어 있습니다.")
            except commands.ExtensionFailed :
                return await ctx.send(f"{cog} 를 불러오지 못했습니다.")
            await ctx.send(f"{cog} 가 로드되었습니다.")

        else:
            await ctx.send("이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.")

    @commands.command(name='코그언로드')
    async def unload(self, ctx, *, cog: str):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.client.unload_extension(f"cogs.{cog}")
            except commands.ExtensionNotLoaded:
                return await ctx.send(f"{cog} 가 언로드상태입니다.")
            except commands.ExtensionFailed :
                return await ctx.send(f"{cog} 를 불러오지 못했습니다.")
            await ctx.send(f"{cog} 가 언로드되었습니다.")

        else:
            await ctx.send("이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.")

    @commands.command(name='코그리로드')
    async def reload(self, ctx, *, cog: str):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.client.reload_extension(f"cogs.{cog}")
            except commands.ExtensionNotLoaded:
                return await ctx.send(f"{cog} 기 로드되어 있지 않습니다.")
            except commands.ExtensionFailed :
                return await ctx.send(f"{cog} 를 불러오지 못했습니다.")
            await ctx.send(f"{cog} 가 로드되었습니다.")

        else:
            await ctx.send("이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.")

    @commands.command(name='코그전체로드')
    async def load_all_cogs(self, ctx):
        if ctx.author.guild_permissions.administrator:
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    try:
                        await self.client.load_extension(f"cogs.{filename[:-3]}")
                        await ctx.reply(f'{filename}가 로드되었습니다.')
                        
                    except commands.ExtensionAlreadyLoaded :
                        await self.client.unload_extension(f"cogs.{filename[:-3]}")
                        await self.client.load_extension(f"cogs.{filename[:-3]}")
                        await ctx.reply(f"{filename}를 재로드 했습니다.")
                        
                    except commands.ExtensionFailed :
                        await ctx.reply(f"{filename}의 로드에 실패하였습니다.")
        else:
            await ctx.send("이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.")
    

async def setup(client):
    await client.add_cog(CogManager(client))