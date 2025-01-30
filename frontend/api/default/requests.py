import asyncio
import json
import random

import aiohttp
from aiohttp import ClientConnectorError, ServerDisconnectedError
from .models import BaseRequestModel


class BaseRequest(object):
    def __init__(self,
                 base_url: str,
                 headers: dict = None,
                 proxy: str = None,
                 timeout: int = 5,
                 debug: bool = False):
        self._base_url = base_url
        self._headers = headers
        self._proxy = proxy
        self._timeout = timeout
        self._debug = debug

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> BaseRequestModel:
        url = f"{self._base_url}/{endpoint}" if endpoint != '' else self._base_url
        if self._debug:
            dict_kwargs = {**kwargs}
            print('[DEBUG] Accepted _proxy:', self._proxy)
            print(f'[DEBUG] Request URL: {url} Params: {dict_kwargs}')
            print(f'[DEBUG] Request Headers: {self._headers}')
        if kwargs.get('data'):
            try:
                json_data = json.loads(kwargs.get('data'))
                del kwargs['data']
                kwargs['json'] = json_data
                self._headers.update({'Content-Type': "application/json; charset=utf-8"})
            except json.decoder.JSONDecodeError:
                self._headers.update({'Content-Type': "text/plain; charset=utf-8"})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method=method, url=url, headers=self._headers,
                                           proxy=self._proxy, timeout=self._timeout, **kwargs) as response:
                    # response.raise_for_status()
                    if self._debug:
                        print(f'[DEBUG] Response URL: {url} Response: {await response.text()}')
                    return BaseRequestModel(text=await response.text(encoding="utf-8"), status_code=response.status,
                                            response=response, read_bytes=await response.read())

        except aiohttp.ClientHttpProxyError:
            print('[DEBUG] Accepted _proxy:', self._proxy)
            return await self._make_request(method, endpoint, **kwargs)

        except asyncio.TimeoutError:
            return await self._make_request(method, endpoint, **kwargs)

        except ClientConnectorError:
            return await self._make_request(method, endpoint, **kwargs)

        except ServerDisconnectedError:
            return await self._make_request(method, endpoint, **kwargs)

    async def _get(self, endpoint: str, params=None, **kwargs) -> BaseRequestModel:
        r"""Sends a GET request.
            :param params: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            """
        return await self._make_request(method="GET", endpoint=endpoint, params=params, **kwargs)

    async def _post(self, endpoint: str, **kwargs) -> BaseRequestModel:
        r"""Sends a POST request.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
        :param json: (optional) A JSON serializable Python object to send in the body.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        return await self._make_request(method="POST", endpoint=endpoint, **kwargs)

    async def _put(self, endpoint: str, **kwargs) -> BaseRequestModel:
        return await self._make_request(method="PUT", endpoint=endpoint, **kwargs)

    async def _delete(self, endpoint: str, **kwargs) -> BaseRequestModel:
        return await self._make_request(method="DELETE", endpoint=endpoint, **kwargs)
