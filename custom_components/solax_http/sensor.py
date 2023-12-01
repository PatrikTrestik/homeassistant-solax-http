import numbers
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import SolaxHttpUpdateCoordinator
from .const import plugin_base
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, replace
import homeassistant.util.dt as dt_util

from .const import ATTR_MANUFACTURER, DOMAIN
from .const import BaseHttpSensorEntityDescription

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass:HomeAssistant, entry, async_add_entities):
    name = entry.options[CONF_NAME]
    coordinator: SolaxHttpUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    plugin:plugin_base=coordinator.plugin

    device_info = {
        "identifiers": {(DOMAIN, name)},
        "name": name,
        "manufacturer": ATTR_MANUFACTURER,
    }

    entities = []

    for sensor_description in plugin.SENSOR_TYPES:
        if plugin.matchWithMask(sensor_description.allowedtypes, sensor_description.blacklist):
            newdescr = sensor_description
            sensor = SolaXHttpSensor(
                coordinator,
                name,
                device_info,
                newdescr,
            )
            entities.append(sensor)

    async_add_entities(entities)

    return True



class SolaXHttpSensor(CoordinatorEntity, SensorEntity):
    """Representation of an SolaX Http sensor."""

    def __init__(
        self,
        coordinator,
        platform_name,
        device_info,
        description: BaseHttpSensorEntityDescription,
    )->None:
        """Initialize the sensor."""
        super().__init__(coordinator, context=description)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: BaseHttpSensorEntityDescription = description
        self._value=None

    async def async_added_to_hass(self):
        """Register callbacks."""
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is not None:
            self._value = self.coordinator.get_data(self.entity_description)
            self.async_write_ha_state()

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._value


