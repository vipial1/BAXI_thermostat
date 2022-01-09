"""The BAXI Thermostat integration."""

from .BaxiAPI import BaxiAPI
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORM
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .config_schema import CONF_PAIR_CODE

PLATFORMS: list[str] = [PLATFORM]


async def async_setup(hass: HomeAssistant, config) -> bool:
    domain_configs = config.get(DOMAIN, [])
    for domain_config in domain_configs:
        if domain_config.get("platform", False) == PLATFORM:
            user = domain_config.get(CONF_USERNAME)
            password = domain_config.get(CONF_PASSWORD)
            pairing_code = domain_config.get(CONF_PAIR_CODE)
            api = BaxiAPI(hass, user, password, pairing_code)
            await api.bootstrap()
            hass.data[PLATFORM] = api
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
