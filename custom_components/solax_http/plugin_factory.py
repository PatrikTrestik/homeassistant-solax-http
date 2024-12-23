"""Module contains the PluginFactory class which is used to create instances of plugins."""

import json
import logging

import aiohttp

from .entity_definitions import (
    BUTTON_TYPES,
    NUMBER_TYPES,
    POW7,
    POW11,
    POW22,
    SELECT_TYPES,
    SENSOR_TYPES,
    TIME_TYPES,
    V10,
    V11,
    V20,
    X1,
    X3,
)
from .plugin_solax_ev_charger import solax_ev_charger_plugin
from .plugin_solax_ev_charger_g2 import solax_ev_charger_plugin_g2

_LOGGER = logging.getLogger(__name__)


class PluginFactory:
    """Factory class to create plugin instances."""

    @staticmethod
    async def _http_post(url, payload, retry=3):
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
                return await PluginFactory._http_post(url, payload, retry - 1)
        except aiohttp.ServerDisconnectedError:
            if retry:
                return await PluginFactory._http_post(url, payload, retry - 1)
        except aiohttp.client_exceptions.ClientOSError:
            if retry > 0:
                return await PluginFactory._http_post(url, payload, retry - 1)
        except Exception as ex:
            _LOGGER.exception("Error reading from Http. Url: %s", url, exc_info=ex)
        return None

    @staticmethod
    async def _read_serial_number(host: str, pwd: str):
        httpData = None
        text = await PluginFactory._http_post(
            f"http://{host}", f"optType=ReadRealTimeData&pwd={pwd}"
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
        return httpData["Information"][2]

    @staticmethod
    def _determine_type(sn: str):
        _LOGGER.info("Trying to determine inverter type")
        invertertype = 0
        # derive invertertupe from seriiesnumber
        # Adding support for G2 HEC
        if sn.startswith("C"):  # G1 EVC
            # Version
            if sn[4] == "0":
                invertertype = invertertype | V10
            elif sn[4] == "1":
                invertertype = invertertype | V11
            # Phases
            if sn[1] == "1":
                invertertype = invertertype | X1
            elif sn[1] == "3":
                invertertype = invertertype | X3
            # Power
            if sn[2:4] == "07":
                invertertype = invertertype | POW7
            elif sn[2:4] == "11":
                invertertype = invertertype | POW11
            elif sn[2:4] == "22":
                invertertype = invertertype | POW22
        elif sn.startswith("50"):  # G2 HEC
            # Version
            invertertype = V20
            # Phases
            if sn[2] == "3":
                invertertype = invertertype | X3
            elif sn[2] == "2":
                invertertype = invertertype | X1
            # Power
            if sn[4] == "B":
                invertertype = invertertype | POW11
            elif sn[4] == "M":
                invertertype = invertertype | POW22
            elif sn[4] == "7":
                invertertype = invertertype | POW7
        else:
            _LOGGER.error("Unrecognized inverter type - serial number: %s", sn)
            return None
        return invertertype

    @staticmethod
    async def get_plugin_instance(host: str, pwd: str):
        """Get an instance of plugin based on serial number/type."""
        sn = await PluginFactory._read_serial_number(host, pwd)
        if sn is None:
            _LOGGER.warning("Attempt to read serialnumber failed")
            return None
        _LOGGER.info("Read serial number: %s", sn)
        invertertype = PluginFactory._determine_type(sn)
        if invertertype:
            if invertertype & V10 or invertertype & V11:
                return solax_ev_charger_plugin(
                    serialnumber=sn,
                    invertertype=invertertype,
                    plugin_name="solax_ev_charger",
                    TIME_TYPES=TIME_TYPES,
                    SENSOR_TYPES=SENSOR_TYPES,
                    NUMBER_TYPES=NUMBER_TYPES,
                    BUTTON_TYPES=BUTTON_TYPES,
                    SELECT_TYPES=SELECT_TYPES,
                )
            if invertertype & V20:
                return solax_ev_charger_plugin_g2(
                    serialnumber=sn,
                    invertertype=invertertype,
                    plugin_name="solax_ev_charger_g2",
                    TIME_TYPES=TIME_TYPES,
                    SENSOR_TYPES=SENSOR_TYPES,
                    NUMBER_TYPES=NUMBER_TYPES,
                    BUTTON_TYPES=BUTTON_TYPES,
                    SELECT_TYPES=SELECT_TYPES,
                )
        raise ValueError(f"Unknown inverter type: {sn}")
