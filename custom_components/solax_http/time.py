import datetime
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.time import TimeEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from .const import ATTR_MANUFACTURER, DOMAIN, BaseHttpTimeEntityDescription
from .plugin_base import plugin_base
from .coordinator import SolaxHttpUpdateCoordinator
from typing import Any, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    name = entry.options[CONF_NAME]
    coordinator: SolaxHttpUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    plugin: plugin_base = coordinator.plugin

    entities = []
    for time_info in plugin.TIME_TYPES:
        if plugin.matchWithMask(time_info.allowedtypes, time_info.blacklist):
            time = SolaXHttpTime(coordinator, name, plugin.device_info, time_info)

            entities.append(time)

    async_add_entities(entities)
    return True


class SolaXHttpTime(CoordinatorEntity, TimeEntity):
    """Representation of an SolaX Http time."""

    def __init__(
        self,
        coordinator: SolaxHttpUpdateCoordinator,
        platform_name,
        device_info,
        description: BaseHttpTimeEntityDescription,
    ) -> None:
        """Initialize the time."""
        super().__init__(coordinator, context=description)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description = description
        self._value: datetime.time = None

    async def async_added_to_hass(self) -> None:
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
    def native_value(self) -> datetime.time:
        return self._value

    async def async_set_value(self, value: datetime.time) -> None:
        """Change the time value."""
        payload = value
        success = await self.coordinator.write_register(
            self.entity_description.register, payload
        )
        await self.coordinator.async_request_refresh()
