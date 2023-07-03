import discord
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
import time

load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

# 티어 순서
TIER_ORDER = [
    'IRON',
    'BRONZE',
    'SILVER',
    'GOLD',
    'PLATINUM',
    'DIAMOND',
    'MASTER',
    'GRANDMASTER',
    'CHALLENGER'
]

class lol_info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.RIOT_API_KEY = RIOT_API_KEY
        self.BASE_URL = 'https://kr.api.riotgames.com'
        self.requests_limit = 0

    async def delay_requests(self):
        # 1초에 최대 20회
        if self.requests_limit == 20:
            await asyncio.sleep(1)
            self.requests_limit = 0
        # 2분에 최대 100회
        elif self.requests_limit == 100:
            await asyncio.sleep(120)
            self.requests_limit = 0

    @commands.command(name='롤')
    async def lol_info_command(self, ctx, summoner_name):
        # 소환사 이름을 입력받아 Riot API를 통해 소환사 정보를 조회
        async def get_summoner_info(summoner_name):
            await self.delay_requests()  # API 호출 제한 체크
            url = f'{self.BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner_name}'
            headers = {'X-Riot-Token': self.RIOT_API_KEY}
            response = requests.get(url, headers=headers)

            self.requests_limit += 1

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                await ctx.send('소환사를 찾을 수 없습니다.')
            else:
                await ctx.send('Riot API에 오류가 발생했습니다.')
            return None

        # 소환사 랭크 정보를 조회
        async def get_rank_info(summoner_id, queue_type):
            await self.delay_requests()  # API 호출 제한 체크
            url = f'{self.BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}'
            headers = {'X-Riot-Token': self.RIOT_API_KEY}
            response = requests.get(url, headers=headers)

            self.requests_limit += 1

            if response.status_code == 200:
                rank_info = response.json()
                for entry in rank_info:
                    if entry['queueType'] == queue_type:
                        return entry
                return None
            elif response.status_code == 404:
                await ctx.send('랭크 정보를 찾을 수 없습니다.')
            else:
                await ctx.send('Riot API에 오류가 발생했습니다.')
            return None

        # 티어 순위 반환
        def get_tier_rank(tier, rank):
            if tier not in TIER_ORDER:
                return None
            tier_order = TIER_ORDER.index(tier)
            if tier_order < len(TIER_ORDER) - 1:
                return f'{tier.capitalize()} {rank}'
            else:
                return rank

        # 소환사 정보 조회
        summoner_info = await get_summoner_info(summoner_name)

        if summoner_info is not None:
            summoner_id = summoner_info['id']

            # 솔로 랭크 정보 조회
            solo_rank_info = await get_rank_info(summoner_id, 'RANKED_SOLO_5x5')

            # 자유 랭크 정보 조회
            flex_rank_info = await get_rank_info(summoner_id, 'RANKED_FLEX_SR')

            embed = discord.Embed(title=f'{summoner_name}님의 소환사 정보', description=f'*{summoner_info["name"]}*', color=discord.Color.blue())
            embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.19.1/img/profileicon/{summoner_info["profileIconId"]}.png')

            if solo_rank_info is not None:
                solo_tier = solo_rank_info['tier']
                solo_rank = solo_rank_info['rank']
                solo_lp = solo_rank_info['leaguePoints']
                solo_wins = solo_rank_info['wins']
                solo_losses = solo_rank_info['losses']
                solo_win_rate = round(solo_wins / (solo_wins + solo_losses) * 100, 2)

                solo_icon_url = f'http://ddragon.leagueoflegends.com/cdn/11.19.1/img/tier/{solo_tier.lower()}_{solo_rank.lower()}.png'
                solo_tier_rank = get_tier_rank(solo_tier, solo_rank)

                embed.add_field(name='솔로 랭크', value=f'{solo_tier_rank}\n{solo_lp} LP\n승: {solo_wins} 패: {solo_losses} 승률: {solo_win_rate}%', inline=True)
                embed.set_thumbnail(url=solo_icon_url)
            else:
                embed.add_field(name='솔로 랭크', value='데이터가 부족합니다.', inline=True)

            if flex_rank_info is not None:
                flex_tier = flex_rank_info['tier']
                flex_rank = flex_rank_info['rank']
                flex_lp = flex_rank_info['leaguePoints']
                flex_wins = flex_rank_info['wins']
                flex_losses = flex_rank_info['losses']
                flex_win_rate = round(flex_wins / (flex_wins + flex_losses) * 100, 2)

                flex_icon_url = f'http://ddragon.leagueoflegends.com/cdn/11.19.1/img/tier/{flex_tier.lower()}_{flex_rank.lower()}.png'
                flex_tier_rank = get_tier_rank(flex_tier, flex_rank)

                embed.add_field(name='자유 랭크', value=f'{flex_tier_rank}\n{flex_lp} LP\n승: {flex_wins} 패: {flex_losses} 승률: {flex_win_rate}%', inline=True)
                embed.set_thumbnail(url=flex_icon_url)
            else:
                embed.add_field(name='자유 랭크', value='데이터가 부족합니다.', inline=True)

            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(lol_info(client))
