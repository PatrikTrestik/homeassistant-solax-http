"""Module provides the base plugin class for Solax HTTP integration."""

from contextlib import suppress
from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntityDescription
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.time import TimeEntityDescription
from homeassistant.helpers.device_registry import DeviceInfo

from .entity_definitions import ALL_POW_GROUP, ALL_VER_GROUP, ALL_X_GROUP

_LOGGER = logging.getLogger(__name__)


@dataclass
class plugin_base:
    """Base plugin class for Solax HTTP integration."""

    plugin_name: str
    TIME_TYPES: list[TimeEntityDescription]
    SENSOR_TYPES: list[SensorEntityDescription]
    BUTTON_TYPES: list[ButtonEntityDescription]
    NUMBER_TYPES: list[NumberEntityDescription]
    SELECT_TYPES: list[SelectEntityDescription]
    device_info: DeviceInfo = None
    invertertype = None
    serialnumber: str = ""
    hw_version: str = "Unknown"
    sw_version: str = "Unknown"

    async def initialize(self) -> None:
        pass

    @property
    def inverter_model(self) -> str:
        return "Unknown"

    def map_data(self, descr, data) -> any:
        return None

    def map_payload(self, address, payload):
        return None

    def _reverse_scale(self, descr, scaled_value):
        """Reverse the scaling process to retrieve the original value."""

        if isinstance(descr.scale, dict):  # translate string back to int
            original_value = next(
                (key for key, val in descr.scale.items() if val == scaled_value), None
            )
        elif callable(descr.scale):  # reverse function call ???
            original_value = scaled_value
        elif isinstance(descr.scale, (int, float)):  # check if scale is a number
            with suppress(Exception):
                original_value = round(scaled_value / descr.scale)
        else:
            original_value = scaled_value
        return original_value

    def _apply_scale(self, descr, value):
        """Apply scale to the value based on the description."""
        return_value = value
        if isinstance(descr.scale, dict):  # translate int to string
            return_value = descr.scale.get(value, "Unknown")
        elif callable(descr.scale):  # function to call ?
            return_value = descr.scale(value, descr)
        elif isinstance(descr.scale, (int, float)): # apply simple numeric scaling and rounding if not a list of words
            with suppress(Exception):
                return_value = round(value * descr.scale, descr.rounding)
        return return_value

    def matchWithMask(self, entitymask, blacklist=None):
        if self.invertertype is None or self.invertertype == 0:
            return False
        # returns true if the entity needs to be created for an inverter
        powmatch = ((self.invertertype & entitymask & ALL_POW_GROUP) != 0) or (
            entitymask & ALL_POW_GROUP == 0
        )
        xmatch = ((self.invertertype & entitymask & ALL_X_GROUP) != 0) or (
            entitymask & ALL_X_GROUP == 0
        )
        vermatch = ((self.invertertype & entitymask & ALL_VER_GROUP) != 0) or (
            entitymask & ALL_VER_GROUP == 0
        )
        blacklisted = False
        if blacklist:
            for start in blacklist:
                if self._serialnumber.startswith(start):
                    blacklisted = True
        return (powmatch and xmatch and vermatch) and not blacklisted
