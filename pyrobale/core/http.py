import aiohttp
from ..exceptions.common import *
from typing import Optional

class HttpClient:
    __session: Optional["aiohttp.ClientSession"] = None
    def __init__(self) -> None:
        self.__session = None
    
    @property
    def ua(self):
        return "pyrobale (https://pyrobale.ir): A simple, useful and lightweight api wrapper for bale bots"
    

    def check_session(self) -> None:
        if not self.__session or self.__session.closed:
            self.__session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(keepalive_timeout=20.0)
            )

    async def make_post(self, url: str, data: Optional[dict] = None) -> dict:
        self.check_session()
        if self.__session is None:
            raise RuntimeError("Session could not be created")

        async with self.__session.post(url, json=data, headers={'User-Agent': self.ua}) as response:
            json_data = await response.json()
            if json_data.get('ok'):
                return json_data
            else:
                error_code = json_data.get('error_code')
                description = json_data.get('description') or 'No description'
                if error_code == 404:
                    raise NotFoundException(f"Error not found 404 : {description}")
                elif error_code == 403:
                    raise ForbiddenException(f"Error Forbidden 403 : {description}")
                else:
                    raise PyroBaleException(f"unknown error : {description}")

    async def make_get(self, url: str, headers: Optional[dict] = None) -> dict:
        self.check_session()
        if self.__session is None:
            raise RuntimeError("Session could not be created")

        async with self.__session.get(url, headers=headers) as response:
            if response.status != 200:
                raise PyroBaleException(f"Unwanted Error from bale: {response.status}")

            json_data = await response.json()
            if json_data.get('ok'):
                return json_data
            else:
                error_code = json_data.get('error_code')
                description = json_data.get('description') or 'No description'
                if error_code == 404:
                    raise NotFoundException(f"Error not found 404 : {description}")
                elif error_code == 403:
                    raise ForbiddenException(f"Error Forbidden 403 : {description}")
                else:
                    raise PyroBaleException(f"unknown error : {description}")

    async def make_via_multipart(self, url: str, data: aiohttp.FormData) -> dict:
        self.check_session()
        async with self.__session.post(url, data=data) as resp:
            json_response = await resp.json()
            if json_response.get('ok'):
                return json_response
            else:
                error_code = json_response.get('error_code', 0)
                description = json_response.get('description', 'No description')

                if error_code == 404:
                    raise NotFoundException(f"Error not found 404 : {description}")
                elif error_code == 403:
                    raise ForbiddenException(f"Error Forbidden 403 : {description}")
                else:
                    raise PyroBaleException(f"Unknown error {error_code}: {description}")
