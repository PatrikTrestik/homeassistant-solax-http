from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.select import SelectEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from .const import ATTR_MANUFACTURER, DOMAIN
from .const import BaseHttpSelectEntityDescription
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
    for select_info in plugin.SELECT_TYPES:
        if plugin.matchWithMask(select_info.allowedtypes, select_info.blacklist):
            select = SolaXHttpSelect(coordinator, name, plugin.device_info, select_info)

            entities.append(select)

    async_add_entities(entities)
    return True


class SolaXHttpSelect(CoordinatorEntity, SelectEntity):
    """Representation of an SolaX Http select."""

    coordinator: SolaxHttpUpdateCoordinator

    def __init__(
        self,
        coordinator: SolaxHttpUpdateCoordinator,
        platform_name,
        device_info,
        description: BaseHttpSelectEntityDescription,
    ) -> None:
        """Initialize the selector."""
        super().__init__(coordinator, context=description)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description = description
        self._attr_options = list(description.scale.values())
        self._value = None

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
    def current_option(self) -> str:
        return self._value

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    async def async_select_option(self, option: str) -> None:
        """Change the select option."""
        await self.coordinator.write_register(self.entity_description, option)
