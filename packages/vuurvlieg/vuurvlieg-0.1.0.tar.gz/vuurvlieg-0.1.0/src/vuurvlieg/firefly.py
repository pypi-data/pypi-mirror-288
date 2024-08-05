"""Firefly client."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self

from aiohttp import ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL


from vuurvlieg.models import AboutResponse, About

from vuurvlieg.exceptions import FireflyError, FireflyConnectionError

VERSION = metadata.version(__package__)


@dataclass
class Vuurvlieg:
    """Main class for handling connections with Firefly."""

    api_host: str
    token: str | None = None
    session: ClientSession | None = None
    request_timeout: int = 10
    _close_session: bool = False

    async def _request(
        self,
        method: str,
        uri: str,
        *,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to Firefly."""
        url = URL(self.api_host).joinpath(f"api/v1{uri}")

        headers = {
            "User-Agent": f"Vuurvlieg/{VERSION}",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        kwargs = {
            "headers": headers,
            "params": params,
            "json": data,
        }

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(method, url, **kwargs)
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to Firefly"
            raise FireflyConnectionError(msg) from exception

        content_type = response.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected response from Firefly"
            raise FireflyError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return await response.text()

    async def _get(self, uri: str, params: dict[str, Any] | None = None) -> str:
        """Handle a GET request to Firefly."""
        return await self._request(METH_GET, uri, params=params)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def get_about(self) -> About:
        """Get information about the Firefly instance."""
        response = await self._get("/about")
        return AboutResponse.from_json(response).data

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Vuurvlieg object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
