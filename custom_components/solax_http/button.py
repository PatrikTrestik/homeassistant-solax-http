import logging
from typing import Optional

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BaseHttpButtonEntityDescription
from .coordinator import SolaxHttpUpdateCoordinator
from .plugin_base import plugin_base

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    name = entry.options[CONF_NAME]
    coordinator: SolaxHttpUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    plugin: plugin_base = coordinator.plugin

    entities = []
    for button_info in plugin.BUTTON_TYPES:
        if plugin.matchWithMask(button_info.allowedtypes, button_info.blacklist):
            button = SolaXHttpButton(coordinator, name, plugin.device_info, button_info)

            entities.append(button)

    async_add_entities(entities)
    return True


class SolaXHttpButton(CoordinatorEntity, ButtonEntity):
    """Representation of an SolaX Http button."""

    coordinator: SolaxHttpUpdateCoordinator

    def __init__(
        self,
        coordinator: SolaxHttpUpdateCoordinator,
        platform_name,
        device_info,
        description: BaseHttpButtonEntityDescription,
    ) -> None:
        """Initialize the selector."""
        super().__init__(coordinator, context=description)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description = description

    async def async_added_to_hass(self):
        """Register callbacks."""
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Button has no state. Do nothing
        pass

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    async def async_press(self) -> None:
        """Write the button value."""
        await self.coordinator.write_register(
            self.entity_description, 1, always=True
        )
