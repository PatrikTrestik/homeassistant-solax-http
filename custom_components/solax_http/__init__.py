"""SolaX Http API Custom Component."""
import logging

from . import plugin_solax_ev_charger
from .coordinator import SolaxHttpUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL

from .const import (
    DOMAIN,
)

PLATFORMS = [
    # "button", "number",
    "select",
    "sensor"]


_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the SolaX Http component."""
    hass.data[DOMAIN] = {}
    _LOGGER.debug("solax data %d", hass.data)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a SolaX Http."""
    _LOGGER.debug(f"setup entries - data: {entry.data}, options: {entry.options}")
    config = entry.options
    name = config[CONF_NAME]

    _LOGGER.debug(f"Setup {DOMAIN}.{name}")

    plugin=plugin_solax_ev_charger.get_plugin_instance()
    coordinator = SolaxHttpUpdateCoordinator(
        hass,
        entry,
        plugin
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload SolaX Http entry."""
    ok=True
    for component in PLATFORMS:
        ok=ok and await hass.config_entries.async_forward_entry_unload(entry, component)
    if not ok:
        return False

    return True

async def config_entry_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)