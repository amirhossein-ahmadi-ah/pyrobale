import aiohttp
from ..exceptions.common import *
from typing import Optional

class HttpClient:
    def __init__(self) -> None:
        self.__session = None
    
    @property
    def ua(self):
        return "pyrobale (https://pyrobale.ir): A simple, useful and lightweight api wrapper for bale bots"
    

    def check_session(self) -> None:
        if (self.__session and self.__session.closed) or not self.__session:
            self.__session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=20.0))

    async def make_post(self, url: str, data: Optional[dict] = None) -> dict:
        self.check_session()
        async with self.__session.post(url, json=data, headers={ 'User-Agent': self.ua }) as response:
            json = await response.json()
            if json['ok']:
                return json
            else:
                if json['error_code'] == 404:
                    raise NotFoundException(f"Error not found 404 : {json['description'] if json['description'] else 'No description returned in error'}")
                elif json['error_code'] == 403:
                    raise ForbiddenException(f"Error Forbidden 403 : {json['description'] if json['description'] else 'No description returned in error'}")
                else:
                    raise PyroBaleException(f"unknown error : {json['description'] if json['description'] else 'No description!'}")


    async def make_get(self, url: str, headers: dict|None = None) -> dict:
        self.check_session()
        async with self.__session.get(url, headers=headers) as response:
            if not response.status == 200:
                raise PyroBaleException("Unwanted Error from bale: "+str(response.status))
            json = await response.json()
            if json['ok']:
                if 'result' in json.keys():
                    return json
                else:
                    if json['error_code'] == 404:
                        raise NotFoundException(f"Error not found 404 : {json['description'] if json['description'] else 'No description returned in error'}")
                    elif json['error_code'] == 403:
                        raise ForbiddenException(f"Error Forbidden 403 : {json['description'] if json['description'] else 'No description returned in error'}")
                    else:
                        raise PyroBaleException(f"unknown error : {json['description'] if json['description'] else 'No description'}")

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
