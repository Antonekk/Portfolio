import asyncio
import aiohttp
from aiohttp import ClientSession
from dotenv import load_dotenv
import os
load_dotenv()


class AsyncRiotAPICaller:
    def __init__(self):
        #szablony
        self.level_return_format = "{name}'s level: {level}"
        self.level_return_error_format = "Problem with fetching {name}'s level: {error}"
        #dane potrzebne do obsługi API
        self.api_key = os.getenv('RIOT_GAMES_API_KEY')
        self.url ='https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }

    async def fetch_account_info(self,session:ClientSession, url, payload):
        async with session.get(url.format(name = payload["summonerName"])) as result:
            res = await result.json()
        return res

    #Dane: Lista nazw graczy w grze League of Legends | Wynik: lista wyników do wyświetlenia
    async def api_get_level_for_summoner_names(self,summoner_names):
        async with ClientSession(headers=self.headers) as session:
            requests = [self.fetch_account_info(session, self.url, {"summonerName": summoner }) for summoner in summoner_names]
            results = await asyncio.gather(*requests)
            summoners = []
            for index,result in enumerate(results):
                if result.get("summonerLevel") is None:
                    summoners.append(self.level_return_error_format.format(name=summoner_names[index], error=result["status"]["message"]))
                else:
                    summoners.append(self.level_return_format.format(name=summoner_names[index], level=result["summonerLevel"]))
            return summoners



