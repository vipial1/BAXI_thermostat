import logging
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
)
from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from datetime import timedelta
from typing import Any, Callable, Dict, Optional
from .const import (
    DOMAIN,
    PLATFORM,
    PRESET_MODES,
    HVAC_MODES,
    DEVICE_MODEL,
    DEVICE_MANUFACTER,
)
from .helper import convert_preset_mode, convert_hvac_mode
from homeassistant.const import (
    CONF_NAME,
    ATTR_TEMPERATURE,
)

from .config_schema import SUPPORT_FLAGS, CLIMATE_SCHEMA
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(CLIMATE_SCHEMA)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:

    """Add BaxiThermostat entities from configuration.yaml."""
    _LOGGER.info(
        "Setup entity coming from configuration.yaml named: %s", config.get(CONF_NAME)
    )

    await async_setup_reload_service(hass, DOMAIN, PLATFORM)
    async_add_entities([BaxiThermostat(hass, config)], update_before_add=True)


class BaxiThermostat(ClimateEntity, RestoreEntity):
    """BaxiThermostat"""

    def __init__(self, hass, config):
        """Initialize the thermostat."""
        super().__init__()
        self.hass = hass
        self._baxi_api = hass.data[DOMAIN]
        self._attr_name = config.get(CONF_NAME)
        self._attr_unique_id = config.get(CONF_NAME)
        self._attr_supported_features = SUPPORT_FLAGS
        self._attr_preset_modes = PRESET_MODES
        self._attr_hvac_modes = HVAC_MODES
        self._attr_hvac_mode = HVAC_MODE_OFF
        self._attr_extra_state_attributes = {}
        self.set_device_info()

    def set_device_info(self):
        info = self._baxi_api.get_device_information()
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            manufacturer=DEVICE_MANUFACTER,
            name=info["name"],
            model=DEVICE_MODEL,
            sw_version=info["softwareVersion"],
            hw_version=info["hardwareVersion"],
        )

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._baxi_api.is_bootstraped()

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attr_extra_state_attributes

    async def async_update(self):
        status = await self._baxi_api.get_status()

        if status:
            self._attr_current_temperature = status["roomTemperature"]["value"]
            self._attr_temperature_unit = status["roomTemperature"]["unit"]
            self._attr_target_temperature = status["roomTemperatureSetpoint"]["value"]
            self._attr_preset_mode = convert_preset_mode(
                status["mode"], status["timeProgram"]
            )
            next_switch = status.get("nextSwitch", None)
            if next_switch:
                self._attr_extra_state_attributes["next_change"] = next_switch["time"]
                self._attr_extra_state_attributes["next_temp"] = next_switch[
                    "roomTemperatureSetpoint"
                ]["value"]

        operating_mode = await self._baxi_api.get_operating_mode()

        if operating_mode:
            self._attr_hvac_mode = convert_hvac_mode(operating_mode["mode"])

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self._baxi_api.set_target_temperature(temperature)
        await self.async_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        _LOGGER.warning("Not implemented yet")
