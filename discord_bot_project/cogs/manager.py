import discord
import asyncio
from discord.ext import commands

class manager(commands.Cog) :
    def __init__(self, client) :
        self.client = client

    @commands.command(aliases=['청소', '삭제'])
    async def clear(self, ctx, number:int):
        if ctx.author.guild_permissions.administrator:
            if number == 0 :
                await ctx.send('0개는 지울 수 없습니다.')
            elif number > 0 :
                await ctx.channel.purge(limit = number + 1)
                msg = await ctx.channel.send(f'{number}개의 메세지를 삭제했습니다..')
                await asyncio.sleep(5)
                await msg.delete()
        else :
            await ctx.reply('권한이 없습니다.')

    @clear.error
    async def clear_error(ctx, error) :
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'삐빅-- 권한이 없습니다.{ctx.author.mention} (ErrorCode: MSGE-01)')

async def setup(client) :
    await client.add_cog(manager(client))
