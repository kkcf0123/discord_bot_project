import discord
import asyncio
from discord.ext import commands

class manager(commands.Cog) :
    def __init__(self, client) :
        self.client = client

    @commands.command(aliases=['청소', '삭제'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, number:int):
        if number == 0 :
            await ctx.send('0개를 어떻게 지워...')
        elif number > 0 :
            await ctx.channel.purge(limit = number + 1)
            msg = await ctx.channel.send(f'내가 {number}개의 메세지를 삭제했다. 킹아!')
            await asyncio.sleep(5)
            await msg.delete()

    @clear.error
    async def clear_error(ctx, error) :
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'삐빅-- 권한이 없습니다.{ctx.author.mention} (ErrorCode: MSGE-01)')
        if isinstance(error, commands.MissingRequiredArgument) :
            await ctx.send('몇개를 지우라는건지 얘기는 해줘야지.. 바보야? (ErrorCode : MSGE-02)')
        if isinstance(error, commands.MissingRequiredAttachment) :
            await ctx.send('몇개를 지우라는건지 얘기는 해줘야지.. 바보야? (ErrorCode : MSGE-03)')

async def setup(client) :
    await client.add_cog(manager(client))
