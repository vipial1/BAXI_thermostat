"""The BAXI Thermostat integration."""

from .BaxiAPI import BaxiAPI
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORM
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .config_schema import CONF_PAIR_CODE

PLATFORMS: list[str] = [PLATFORM]


async def async_setup(hass: HomeAssistant, config) -> bool:
    platform_configs = config.get(PLATFORM, [])
    for platform_config in platform_configs:
        if platform_config.get("platform", False) == DOMAIN:
            user = platform_config.get(CONF_USERNAME)
            password = platform_config.get(CONF_PASSWORD)
            pairing_code = platform_config.get(CONF_PAIR_CODE)
            api = BaxiAPI(hass, user, password, pairing_code)
            await api.bootstrap()
            hass.data[DOMAIN] = api
            return True
    return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)
