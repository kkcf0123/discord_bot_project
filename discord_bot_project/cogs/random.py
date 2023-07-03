import discord
import random
import asyncio
from typing import List
from discord.ext import commands

class random_team(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel = {
            'lobby': None,
            'ATeam': None,
            'BTeam': None,
            'CTeam': None
        }
        # self.command_lock = asyncio.Lock()  # Lock 객체 생성
    
    def filter_bots(self, members: List) -> List:
        return [member for member in members if not member.bot]
    
    def filter_mobile(self, members):
        return [member for member in members if not member.is_on_mobile()]
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='내전채널')
    async def set_channels(self, ctx, lobby_channel: discord.VoiceChannel, ATeam_channel: discord.VoiceChannel, BTeam_channel: discord.VoiceChannel, CTeam_channel: discord.VoiceChannel):
        self.channel['lobby'] = lobby_channel.id
        self.channel['ATeam'] = ATeam_channel.id
        self.channel['BTeam'] = BTeam_channel.id
        self.channel['CTeam'] = CTeam_channel.id
        await ctx.send('채널 ID가 설정되었습니다.')

    @commands.cooldown(1, 3, commands.BucketType.user)
    # @lock_command()
    @commands.command(name='로비')
    async def lobby(self, ctx):
                lobby_vc = self.client.get_channel(self.channel['lobby'])
                ATeam_vc = self.client.get_channel(self.channel['ATeam'])
                Bteam_vc = self.client.get_channel(self.channel['BTeam'])
                Cteam_vc = self.client.get_channel(self.channel['CTeam'])
                A_Team_members = ATeam_vc.members
                B_Team_members = Bteam_vc.members
                C_Team_members = Cteam_vc.members

                members_without_bots = self.filter_bots(ctx.author.voice.channel.members)

                if ctx.author.voice is None:
                    await ctx.send(f'{ctx.author.nick}님, 음성 채널에 먼저 입장해주세요.')
                    return

                # members이 11명 이상인 경우 10명 나누고 1초 쉼
                if not ctx.author.voice.channel == lobby_vc:
                    if not A_Team_members and not B_Team_members and not C_Team_members:
                        for idx, member in enumerate(members_without_bots):
                            await member.move_to(lobby_vc)
                            if (idx + 1) % 10 == 0:
                                await asyncio.sleep(1)

                    if C_Team_members:
                        for idx, member in enumerate(C_Team_members):
                            await member.move_to(lobby_vc)
                            if (idx + 1) % 10 == 0:
                                await asyncio.sleep(1)

                    if A_Team_members:
                        for idx, member in enumerate(A_Team_members):
                            await member.move_to(lobby_vc)
                            if (idx + 1) % 10 == 0:
                                await asyncio.sleep(1)
                            
                    if B_Team_members:
                        for idx, member in enumerate(B_Team_members):
                            await member.move_to(lobby_vc)
                            if (idx + 1) % 10 == 0:
                                await asyncio.sleep(1)
                else:
                    await ctx.send('이미 광장에 모여있네요.')

    @commands.cooldown(1, 3, commands.BucketType.user)
    # @lock_command()
    @commands.command(name='내전')
    async def shuffle(self, ctx, delay=5):
            lobby_vc = self.client.get_channel(self.channel['lobby'])
            ATeam_vc = self.client.get_channel(self.channel['ATeam'])
            Bteam_vc = self.client.get_channel(self.channel['BTeam'])

            members_without_bots = self.filter_bots(ctx.author.voice.channel.members)

            try:
                if ctx.author.voice is None:
                    await ctx.send(f'{ctx.author.nick}님, 음성 채널에 먼저 입장해주세요.')
                    return

                if len(members_without_bots) < 8:
                    await ctx.send(f'현재 음성 채널에는 {len(members_without_bots)}명만 있습니다. 최소 8명 이상이 필요합니다.')
                    return

                if not ctx.author.voice.channel == lobby_vc:
                    await ctx.send(f'{delay}초 뒤에 광장으로 이동합니다.')
                    await asyncio.sleep(delay)
                    for member in members_without_bots:  # move_to lobby
                        await member.move_to(lobby_vc)
                        await asyncio.sleep(1)
                else:
                    await ctx.send('이미 광장에 모여있네요.')

                random.shuffle(members_without_bots)
                members_without_bots = members_without_bots[:10]
                await asyncio.sleep(5)

                mbed = discord.Embed(title='지는팀 니네팀', colour=0x8a9dff)
                mbed.add_field(name='A팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(0, len(members_without_bots), 2)]), inline=True)
                mbed.add_field(name='B팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(1, len(members_without_bots), 2)]), inline=True)

                await ctx.send(embed=mbed)
                await ctx.send('슬슬 대화 마무리해요. `10초` 후에 음성 채널을 나눌게요.')
                await asyncio.sleep(10)

                mobile_members = [member for member in members_without_bots if member.is_on_mobile()]
                for i, member in enumerate(members_without_bots):
                    # ATeam
                    if i % 2 == 0:
                        await member.move_to(ATeam_vc)
                    # Bteam
                    else:
                        await member.move_to(Bteam_vc)
                    if i >= 10 and (i + 1) % 10 == 0:
                        await asyncio.sleep(1)

                # 모바일 멤버들 따로 분류한 후 팀이동
                for i, member in enumerate(mobile_members):
                    # ATeam
                    if i % 2 == 0:
                        await member.move_to(ATeam_vc)
                    # Bteam
                    else:
                        await member.move_to(Bteam_vc)

                await ctx.send('고생하셨어요!')

            except discord.ClientException:
                await ctx.send('오류가 발생했습니다.')
                
                
    @commands.cooldown(1, 3, commands.BucketType.user)
    # @lock_command()
    @commands.command(name='6내전')
    async def six_shuffle(self, ctx, delay=5):
            lobby_vc = self.client.get_channel(self.channel['lobby'])
            ATeam_vc = self.client.get_channel(self.channel['ATeam'])
            BTeam_vc = self.client.get_channel(self.channel['BTeam'])
            CTeam_vc = self.client.get_channel(self.channel['CTeam'])

            members_without_bots = self.filter_bots(ctx.author.voice.channel.members)

            try:
                if ctx.author.voice is None:
                    await ctx.send(f'{ctx.author.nick}님, 음성 채널에 먼저 입장해주세요.')
                    return

                if len(members_without_bots) < 6:
                    await ctx.send(f'현재 음성 채널에는 {len(members_without_bots)}명만 있습니다. 최소 6명 이상이 필요합니다.')
                    return

                if not ctx.author.voice.channel == lobby_vc:
                    await ctx.send(f'{delay}초 뒤에 광장으로 이동합니다.')
                    await asyncio.sleep(delay)
                    for member in members_without_bots:  # move_to lobby
                        await member.move_to(lobby_vc)
                        await asyncio.sleep(1)
                else:
                    await ctx.send('이미 광장에 모여있네요.')

                random.shuffle(members_without_bots)
                members_without_bots = members_without_bots[:6]
                await asyncio.sleep(5)

                mbed = discord.Embed(title='지는팀 니네팀', colour=0x8a9dff)
                mbed.add_field(name='A팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(0, len(members_without_bots), 2)]), inline=True)
                mbed.add_field(name='B팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(1, len(members_without_bots), 2)]), inline=True)
                mbed.add_field(name='C팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(2, len(members_without_bots), 2)]), inline=True)
                
                await ctx.send(embed=mbed)
                await ctx.send('슬슬 대화 마무리해요. `10초` 후에 음성 채널을 나눌게요.')
                await asyncio.sleep(10)

                mobile_members = self.filter_mobile(members_without_bots)
                for i, member in enumerate(members_without_bots):
                    if i < 2:
                        await member.move_to(ATeam_vc)  # A팀
                    elif i < 4:
                        await member.move_to(BTeam_vc)  # B팀
                    else:
                        await member.move_to(CTeam_vc)  # C팀
                await asyncio.sleep(1)
                        
                # 나머지 멤버들 중에서 2명씩 랜덤으로 조합하여 C팀으로 이동
                random.shuffle(mobile_members)
                for i, member in enumerate(mobile_members):
                    await member.move_to(ATeam_vc)  # A팀으로 이동
                    if i >= 2 and (i + 1) % 2 == 0:
                        await asyncio.sleep(1)

                await ctx.send('고생하셨어요!')

            except discord.ClientException:
                await ctx.send('오류가 발생했습니다.')
                
    @commands.cooldown(1, 3, commands.BucketType.user)
    # @lock_command()
    @commands.command(name='테스트내전')
    async def test_shuffle(self, ctx, delay=5):
        async with self.command_lock:  # Lock 획득
            lobby_vc = self.client.get_channel(self.channel['lobby'])
            ATeam_vc = self.client.get_channel(self.channel['ATeam'])
            Bteam_vc = self.client.get_channel(self.channel['BTeam'])

            members_without_bots = self.filter_bots(ctx.author.voice.channel.members)

            try:
                if ctx.author.voice is None:
                    await ctx.send(f'{ctx.author.nick}님, 음성 채널에 먼저 입장해주세요.')
                    return

                if len(members_without_bots) < 8:
                    await ctx.send(f'현재 음성 채널에는 {len(members_without_bots)}명만 있습니다. 최소 8명 이상이 필요합니다.')
                    return

                if not ctx.author.voice.channel == lobby_vc:
                    await ctx.send(f'{delay}초 뒤에 광장으로 이동합니다.')
                    await asyncio.sleep(delay)
                    for member in members_without_bots:  # move_to lobby
                        await member.move_to(lobby_vc)
                        await asyncio.sleep(1)
                else:
                    await ctx.send('이미 광장에 모여있네요.')

                random.shuffle(members_without_bots)
                members_without_bots = members_without_bots[:10]
                await asyncio.sleep(5)

                mbed = discord.Embed(title='지는팀 니네팀', colour=0x8a9dff)
                mbed.add_field(name='A팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(0, len(members_without_bots), 2)]), inline=True)
                mbed.add_field(name='B팀', value='\n'.join([f'**{members_without_bots[i].nick}**' for i in range(1, len(members_without_bots), 2)]), inline=True)

                await ctx.send(embed=mbed)
                await ctx.send('슬슬 대화 마무리해요. `10초` 후에 음성 채널을 나눌게요.')
                await asyncio.sleep(10)

                # A팀으로 이동
                for i in range(0, len(members_without_bots), 5):
                    a_team_members = members_without_bots[i:i+5]
                    for member in a_team_members:
                        await member.move_to(ATeam_vc)
                    await asyncio.sleep(1)

                # B팀으로 이동
                for i in range(1, len(members_without_bots), 5):
                    b_team_members = members_without_bots[i:i+5]
                    for member in b_team_members:
                        await member.move_to(Bteam_vc)
                    await asyncio.sleep(1)

                await ctx.send('고생하셨어요!')

            except discord.ClientException:
                await ctx.send('오류가 발생했습니다.')

async def setup(client):
    await client.add_cog(random_team(client))
