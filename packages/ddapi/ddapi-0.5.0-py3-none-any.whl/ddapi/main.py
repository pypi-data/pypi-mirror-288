import re
from datetime import datetime
from typing import Union
from urllib.parse import quote

from .dataclass import DDPlayer, Master, Player, Query, STPlayer, STServers, STServer, STClients, STClans, STGameTypes, \
    STMaps, STVersions, STMastersStats, STBans, DMap, DDStatsSql, DDStatus
from .deflt import API

REG_SERVER = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

__all__ = (
    "utc_times",
    "DDnetApi",
    "DDstats",
    "StatusAPI",
    "DDStatsDB"
)


def utc_times(timestamp: int | float) -> datetime:
    return datetime.utcfromtimestamp(timestamp)


class DDStatsDB(API):
    @staticmethod
    def powered() -> str:
        return 'ddstats.org'

    async def _rt(self, url: str):
        return await self._generate(url, DDStatsSql)

    async def next(self, dd: DDStatsSql):
        return await self._rt(dd.next_url)

    async def sql(self, sql: str):
        return await self._rt(f"https://db.ddstats.org/ddnet-7b306cf?sql={quote(sql)}")

    async def mapinfo(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/mapinfo.json")

    async def teamrace(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/teamrace.json")

    async def race(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/race.json")

    async def maps(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/maps.json")


class DDnetApi(API):
    @staticmethod
    def powered() -> str:
        return 'ddnet.org'

    async def player(self, player: str) -> Union[DDPlayer, None]:
        return await self._generate(f"https://ddnet.org/players/?json2={quote(player)}", DDPlayer,
                                    emoji=self._get_emoji(player))

    async def status(self) -> Union[DDStatus, None]:
        return await self._generate("https://ddnet.org/status/json/stats.json", DDStatus)

    async def query(self, player: str) -> Union[Query, None]:
        return await self._generate(f"https://ddnet.org/players/?query={quote(player)}", Query, "data",
                                    emoji=self._get_emoji(player))

    async def master(self) -> Union[Master, None]:
        return await self._generate("https://master1.ddnet.org/ddnet/15/servers.json", Master)

    async def map(self, map_name: str) -> Union[DMap, None]:
        return await self._generate(f"https://ddnet.org/maps/?json={quote(map_name)}", DMap)


class DDstats(API):
    @staticmethod
    def powered() -> str:
        return 'ddstats.tw'

    async def player(self, nickname) -> Union[Player, None]:
        return await self._generate(f"https://ddstats.tw/player/json?player={quote(nickname)}", Player,
                                    emoji=self._get_emoji(nickname))


class StatusAPI(API):
    @staticmethod
    def powered() -> str:
        return 'status.tw'

    async def player(self, nickname) -> Union[STPlayer, None]:
        return await self._generate(f"https://api.status.tw/player/details/{quote(nickname)}", STPlayer,
                                    emoji=self._get_emoji(nickname))

    async def server(self, ip: str, port: int) -> Union[STServer, None]:
        if not re.search(REG_SERVER, ip):
            return
        return await self._generate(f"https://api.status.tw/server/details/{ip}/{port}", STServer)

    async def players(self) -> Union[STClients, None]:
        return await self._generate("https://api.status.tw/player/list", STClients, "players")

    async def servers(self) -> Union[STServers, None]:
        return await self._generate("https://api.status.tw/server/list/", STServers, "servers")

    async def clans(self) -> Union[STClans, None]:
        return await self._generate("https://api.status.tw/clan/list", STClans, "clans")

    async def gametype(self) -> Union[STGameTypes, None]:
        return await self._generate("https://api.status.tw/gametype/list", STGameTypes, "gametypes")

    async def maps(self) -> Union[STMaps, None]:
        return await self._generate("https://api.status.tw/map/list", STMaps, "maps")

    async def bans(self) -> Union[STBans, None]:
        return await self._generate("https://api.status.tw/master/ban/list", STBans, "bans")

    async def versions(self) -> Union[STVersions, None]:
        return await self._generate("https://api.status.tw/version/list", STVersions, "versions")

    async def masters_stats(self) -> Union[STMastersStats, None]:
        return await self._generate("https://api.status.tw/master/stats", STMastersStats, "masters")
