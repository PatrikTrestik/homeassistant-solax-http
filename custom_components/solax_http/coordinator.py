import asyncio
from datetime import timedelta
import json
import logging
import aiohttp

import async_timeout
from .plugin_base import plugin_base
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_SN,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    REQUEST_REFRESH_DELAY,
    API_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


class SolaxHttpUpdateCoordinator(DataUpdateCoordinator[None]):
    config_entry: ConfigEntry

    def __init__(
        self, hass: HomeAssistant, config: ConfigEntry, plugin: plugin_base
    ) -> None:
        """Initialize Solax Http API data updater."""

        _LOGGER.debug("Setting up coordinator")
        self._host = config.options.get(CONF_HOST, None)
        self._sn = config.options.get(CONF_SN, None)
        self.plugin = plugin

        scan_interval = config.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self._host}",
            update_interval=timedelta(seconds=scan_interval),
            request_refresh_debouncer=Debouncer(
                hass,
                _LOGGER,
                cooldown=REQUEST_REFRESH_DELAY,
                immediate=False,
            ),
        )

    async def _async_update_data(self):
        """Fetch data from SolaX Http Api."""

        try:
            # This timeout is only a safeguard against the API methods locking
            # up. The API methods themselves have their own timeouts.
            async with async_timeout.timeout(10 * API_TIMEOUT):
                # Fetch updates
                data = await self.__async_get_data()
                if self.plugin.invertertype is None:
                    await self.plugin.initialize(data)
                return data

        except SolaXApiError as err:
            _LOGGER.exception(
                "Fetching data failed: %s: %s", type(err).__qualname__, err
            )
            raise UpdateFailed(err) from err

    def get_data(self, descr):
        return self.plugin.map_data(descr, self.data)

    async def __async_get_data(self) -> dict:
        # Grab active context variables to limit data required to be fetched from API
        # Note: using context is not required if there is no need or ability to limit
        # data retrieved from API.
        contexts = self.async_contexts()
        try:
            realtimeData = await self._read_realtime_data()
            setData = await self._read_set_data()
            if setData is None:
                setData = []
            if realtimeData is None:
                realtimeData = {"Data": [], "Information": []}
        except Exception:
            _LOGGER.exception("Something went wrong reading from Http API")

        data = {
            "Set": dict(enumerate(setData)),
            "Data": dict(enumerate(realtimeData["Data"])),
            "Info": dict(enumerate(realtimeData["Information"])),
        }
        return data

    async def _read_realtime_data(self):
        httpData = None
        text = await self._http_post(
            f"http://{self._host}", f"optType=ReadRealTimeData&pwd={self._sn}"
        )
        if text is None:
            return None
        if "failed" in text:
            _LOGGER.error("Failed to read data from http: %s", text)
            return None
        try:
            httpData = json.loads(text)
        except json.decoder.JSONDecodeError:
            _LOGGER.error("Failed to decode json: %s", text)
        return httpData

    async def write_register(self, address, payload):
        """Write register through http."""

        descr = self.plugin.map_payload(address, payload)
        if descr is None:
            return False

        resp = await self._http_post(
            f"http://{self._host}",
            f'optType=setReg&pwd={self._sn}&data={{"num":1,"Data":{json.dumps(descr)}}}',
        )
        if resp is not None:
            _LOGGER.info("Received HTTP API response %s", resp)
            return True
        return False

    async def _read_set_data(self):
        setData = None
        text = await self._http_post(
            f"http://{self._host}", f"optType=ReadSetData&pwd={self._sn}"
        )
        if text is None:
            return None
        if "failed" in text:
            _LOGGER.error("Failed to read data from http: %s", text)
            return None
        try:
            setData = json.loads(text)
        except json.decoder.JSONDecodeError:
            _LOGGER.error("Failed to decode json: %s", text)
        return setData

    async def _http_post(self, url, payload, retry=3):
        try:
            connector = aiohttp.TCPConnector(
                force_close=True,
            )
            async with (
                aiohttp.ClientSession(connector=connector) as session,
                session.post(url, data=payload) as resp,
            ):
                if resp.status == 200:
                    return await resp.text()
        except TimeoutError:
            if retry > 0:
                return await self._http_post(url, payload, retry - 1)
        except aiohttp.ServerDisconnectedError:
            if retry:
                return await self._http_post(url, payload, retry - 1)
        except aiohttp.client_exceptions.ClientOSError:
            if retry > 0:
                return await self._http_post(url, payload, retry - 1)
        except Exception as ex:
            _LOGGER.exception("Error reading from Http. Url: %s", url, exc_info=ex)
        return None


class SolaXApiError(Exception):
    """Base exception for all SolaX API errors."""
