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
from .const import DOMAIN, PLATFORM, PRESET_MODES, HVAC_MODES
from .helper import convert_preset_mode, convert_hvac_mode
from homeassistant.const import (
    CONF_NAME,
    CONF_USERNAME,
    CONF_PASSWORD,
    ATTR_TEMPERATURE,
)

from .config_schema import SUPPORT_FLAGS, CLIMATE_SCHEMA, CONF_PAIR_CODE
from .BaxiAPI import BaxiAPI

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

        user = config.get(CONF_USERNAME)
        password = config.get(CONF_PASSWORD)
        pairing_code = config.get(CONF_PAIR_CODE)

        self.baxi_api = BaxiAPI(hass, user, password, pairing_code)
        self._name = config.get(CONF_NAME)
        self._target_temp = 22
        self._cur_temp = 18
        self._attrs: Dict[str, Any] = {}
        self._state = None
        self._unit = hass.config.units.temperature_unit
        self._support_flags = SUPPORT_FLAGS
        self._preset_mode_list = PRESET_MODES
        self._attr_preset_mode = None
        self._attr_hvac_modes = HVAC_MODES
        self._attr_hvac_mode = HVAC_MODE_OFF

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the thermostat."""
        return self._name

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temp

    @property
    def current_temperature(self):
        """Return the sensor temperature."""
        return self._cur_temp

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.baxi_api.is_bootstraped()

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def preset_modes(self) -> list[str]:
        """Return the list of available preset modes."""
        return self._preset_mode_list

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attrs

    @property
    def hvac_mode(self) -> str:
        """Return current operation."""
        return self._attr_hvac_mode

    async def async_update(self):
        await self.baxi_api.bootstrap()
        status = await self.baxi_api.get_status()

        if status:
            self._cur_temp = status["roomTemperature"]["value"]
            self._unit = status["roomTemperature"]["unit"]
            self._target_temp = status["roomTemperatureSetpoint"]["value"]
            self._attr_preset_mode = convert_preset_mode(
                status["mode"], status["timeProgram"]
            )

        operating_mode = await self.baxi_api.get_operating_mode()

        if operating_mode:
            self._attr_hvac_mode = convert_hvac_mode(operating_mode["mode"])
            self._state = self._attr_hvac_mode

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self.baxi_api.set_target_temperature(temperature)
        await self.async_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        _LOGGER.warning("Not implemented yet")
