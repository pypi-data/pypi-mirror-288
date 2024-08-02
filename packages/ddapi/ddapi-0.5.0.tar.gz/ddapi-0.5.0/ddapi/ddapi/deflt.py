from abc import ABC
from typing import Union, Any

import aiohttp
from aiohttp import ClientSession, ClientConnectorError
from aiohttp.typedefs import DEFAULT_JSON_DECODER, JSONDecoder


class API(ABC):
    def __init__(self,
                 session: ClientSession = None,
                 json_loads: JSONDecoder = DEFAULT_JSON_DECODER,
                 emojis: dict[str, str] = None):
        self.emojis = emojis
        if emojis is None:
            self.emojis = {"fox": "🦊"}
        self.session = session
        self.json_loads = json_loads
        self.url = "https://ddstats.qwik.space/player/json?player={0}"

    def __del__(self):
        self.session = None

    @staticmethod
    def powered() -> str:
        return ''

    def _get_emoji(self, player_name: str) -> str:
        for name, emoji in self.emojis.items():
            if name in player_name.lower():
                return emoji
        return ''

    def closed(self):
        return self.session.closed is None or self.session.closed

    async def _send(self, url: str) -> Union[dict, None]:
        if self.session is None:
            self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(url) as req:
                if req.status == 200:
                    usr = await req.text()
                    if usr == '{}' or usr is None:
                        return
                    del usr
                    return await req.json(loads=self.json_loads)
                return
        except ClientConnectorError:
            return

    async def _generate(self, url: str, model, k: str = None, emoji: str = None) -> Any:
        dat = await self._send(url)
        if dat is None:
            return
        if k is not None:
            dat = {k: dat}
        if emoji is not None:
            dat["emoji"] = emoji
        return model(**dat)

    async def close(self) -> None:
        return await self.session.close()
