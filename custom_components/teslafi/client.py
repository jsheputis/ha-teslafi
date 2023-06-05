"""TeslaFi API Client"""

import httpx
import logging

from .model import TeslaFiVehicle

REQUEST_TIMEOUT = 5
_LOGGER = logging.getLogger(__name__)


class TeslaFiClient:
    """TeslaFi API Client"""

    _api_key: str
    _client: httpx.AsyncClient

    def __init__(
        self,
        api_key: str,
        client: httpx.AsyncClient,
    ) -> None:
        """
        Creates a new TeslaFi API Client.

        :param api_key: API Key can be obtained from https://www.teslafi.com/api.php
        """
        self._api_key = api_key
        self._client = client

    async def last_good(self) -> TeslaFiVehicle:
        """
        Return last data point with charge data
        """
        return TeslaFiVehicle(await self._request("lastGood"))

    async def command(self, cmd: str) -> bool:
        """
        Execute a command.
        See list of commands at https://teslafi.com/api.php
        """
        return await self._request(cmd)


    async def _request(self, command: str = "") -> dict:
        """
        :param command: The command to send. Can be empty string, `lastGood`, etc. See
        """
        response = await self._client.get(
            url="https://www.teslafi.com/feed.php",
            headers={"Authorization": "Bearer " + self._api_key},
            params={"command": command},
            timeout=REQUEST_TIMEOUT,
        )
        assert response.status_code < 400
        data = response.json()
        return data
