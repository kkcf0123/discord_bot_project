import discord
import asyncio
import os
from discord import Embed
from discord.ext import commands

class CogManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.permission_error = '이 명령어는 관리자 권한이 있는 사용자만 실행할 수 있습니다.'
        self.delay = 5
        
    @commands.command(name='코그리스트')
    async def check_cogs(self, ctx, loaded_cog=None, unloaded_cog=None):
        if ctx.author.guild_permissions.administrator:
            cogs_folder_path = "./cogs"
            all_cogs = []

            for filename in os.listdir(cogs_folder_path):
                if filename.endswith(".py"):
                    cog_name = filename[:-3]
                    all_cogs.append(cog_name)

            loaded_cogs = list(self.client.extensions.keys())
            loaded_cogs_without_prefix = [cog.replace("cogs.", "") for cog in loaded_cogs]
            unloaded_cogs = [cog for cog in all_cogs if cog not in loaded_cogs_without_prefix]

            embed = Embed(title="Cogs Status", colour=discord.Colour.green())
            
            embed.add_field(name=":yellow_circle: 전체 Cogs :yellow_circle:", value="\n".join(all_cogs), inline=True)
            if loaded_cog is None:
                loaded_cogs_formatted = "\n".join(loaded_cogs_without_prefix)
                embed.add_field(name=":green_circle: load된 Cogs :green_circle:", value=loaded_cogs_formatted, inline=True)
            elif loaded_cog in loaded_cogs_without_prefix:
                loaded_cogs_without_prefix.remove(loaded_cog)
                loaded_cogs_formatted = "\n".join(loaded_cogs_without_prefix + [f"**{loaded_cog}**"])
                embed.add_field(name=":green_circle: load된 Cogs :green_circle:", value=loaded_cogs_formatted, inline=True)

            if unloaded_cog is None:
                unloaded_cogs_formatted = "\n".join(unloaded_cogs)
                embed.add_field(name=":red_circle: Unload된 Cogs :red_circle:", value=unloaded_cogs_formatted, inline=True)
            elif unloaded_cog in all_cogs:
                unloaded_cogs.remove(unloaded_cog)
                unloaded_cogs_formatted = "\n".join(unloaded_cogs + [f"**{unloaded_cog}**"])
                embed.add_field(name=":red_circle: Unload된 Cogs :red_circle:", value=unloaded_cogs_formatted, inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(self.permission_error)

            
    @commands.command(name='코그로드')
    async def load(self, ctx, *, cog: str):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.client.load_extension(f"cogs.{cog}")
            except commands.ExtensionAlreadyLoaded:
                error_msg = await ctx.send(f"{cog} 가 이미 로드되어 있습니다.")
                await asyncio.sleep(self.delay)
                await error_msg.delete()
                return
            except commands.ExtensionFailed :
                error_msg = await ctx.send(f"{cog} 를 불러오지 못했습니다.")
                await asyncio.sleep(self.delay)
                await error_msg.delete()
                return 
            msg = await ctx.send(f"{cog} 가 로드되었습니다.")
            await self.check_cogs(ctx, loaded_cog=cog)  # 로드된 Cog를 반영하기 위해 check_cogs 실행
            await asyncio.sleep(self.delay)
            await msg.delete()
        else:
            await ctx.send(self.permission_error)
            

    @commands.command(name='코그언로드')
    async def unload(self, ctx, *, cog: str):
        if ctx.author.guild_permissions.administrator:
            try:
                await self.client.unload_extension(f"cogs.{cog}")
            except commands.ExtensionNotLoaded:
                msg = await ctx.send(f"{cog} 가 언로드상태입니다.")
                await asyncio.sleep(self.delay)
                await msg.delete()
                return 
            except commands.ExtensionFailed :
                error_msg = await ctx.send(f"{cog} 를 불러오지 못했습니다.")
                await asyncio.sleep(self.delay)
                await error_msg.delete()
                return 
            msg = await ctx.send(f"{cog} 가 언로드되었습니다.")
            await self.check_cogs(ctx, unloaded_cog=cog)
            await asyncio.sleep(self.delay)
            await msg.delete()
        else:
            await ctx.send(self.permission_error)

    @commands.command(name='코그리로드')
    async def reload(self, ctx, *, cog: str):
            if ctx.author.guild_permissions.administrator:
                try:
                    await self.client.reload_extension(f"cogs.{cog}")
                    msg = await ctx.send(f"{cog} 가 로드되었습니다.")
                    await asyncio.sleep(self.delay)
                    await msg.delete()
                except commands.ExtensionNotLoaded:
                    try:
                        await self.client.load_extension(f"cogs.{cog}")
                        await self.client.reload_extension(f"cogs.{cog}")
                        msg = await ctx.send(f"{cog} 가 로드되었습니다.")
                        await asyncio.sleep(self.delay)
                        await msg.delete()
                    except commands.ExtensionFailed:
                        error_msg = await ctx.send(f"{cog}를 불러오지 못했습니다.")
                        await asyncio.sleep(self.delay)
                        await error_msg.delete()
                        return
                except commands.ExtensionFailed:
                    error_msg = await ctx.send(f"{cog}를 불러오지 못했습니다.")
                    await asyncio.sleep(self.delay)
                    await error_msg.delete()
                    return
            else:
                await ctx.send(self.permission_error)

    @commands.command(name='코그전체로드')
    async def load_all_cogs(self, ctx):
        if ctx.author.guild_permissions.administrator:
            success_cogs = []
            failed_cogs = []

            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    try:
                        await self.client.load_extension(f"cogs.{filename[:-3]}")
                        await success_cogs.append(filename[:-3])
                    except commands.ExtensionAlreadyLoaded:
                        await self.client.unload_extension(f"cogs.{filename[:-3]}")
                        await self.client.load_extension(f"cogs.{filename[:-3]}")
                        await success_cogs.append(filename[:-3])
                    except commands.ExtensionFailed:
                        await failed_cogs.append(filename[:-3])

            embed = discord.Embed(title="Cog Status", colour=discord.Colour.green())
            embed.add_field(name=":green_circle: 성공 :green_circle:", value="\n".join(success_cogs) if success_cogs else "없음", inline=True)
            embed.add_field(name=":red_circle: 실패 :red_circle:", value='"\n".join(failed_cogs)' if failed_cogs else "없음", inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(self.permission_error)

async def setup(client):
    await client.add_cog(CogManager(client))
