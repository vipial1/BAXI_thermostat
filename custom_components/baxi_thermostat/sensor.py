import logging
from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from datetime import timedelta
from typing import Callable, Optional
from .const import *
from homeassistant.const import (
    CONF_NAME,
)

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:

    config = hass.data[PLATFORM].get(DAYA_KEY_CONFIG)

    """Add BaxiEnergyConsumptionSensor entities from configuration.yaml."""
    _LOGGER.info(
        "Setup entity coming from configuration.yaml named: %s", config.get(CONF_NAME)
    )

    await async_setup_reload_service(hass, "sensor", PLATFORM)
    async_add_entities(
        [
            HeaterBaxiEnergyConsumptionSensor(hass, config),
            HotWaterBaxiEnergyConsumptionSensor(hass, config),
        ],
        update_before_add=True,
    )


class BaxiEnergyConsumptionSensor(SensorEntity, RestoreEntity):
    """BaxiEnergyConsumptionSensor"""

    def __init__(self, hass, consumption_type):
        """Initialize the sensor."""
        super().__init__()
        self.hass = hass
        self._baxi_api = hass.data[PLATFORM].get(DATA_KEY_API)
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_should_poll = True
        self._consumption_type = consumption_type

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._baxi_api.is_bootstraped()

    async def async_update(self):
        consumptions = await self._baxi_api.get_consumptions()
        consumption = consumptions[self._consumption_type]
        self._attr_native_unit_of_measurement = consumption["unit"]
        self._attr_native_value = int(consumption["value"])


class HeaterBaxiEnergyConsumptionSensor(BaxiEnergyConsumptionSensor):
    def __init__(self, hass, config):
        """Initialize the sensor."""
        super().__init__(hass, "energyCH")
        self._attr_name = config.get(CONF_NAME) + " Heating consumption"
        self._attr_unique_id = self._attr_name


class HotWaterBaxiEnergyConsumptionSensor(BaxiEnergyConsumptionSensor):
    def __init__(self, hass, config):
        """Initialize the sensor."""
        super().__init__(hass, "energyDHW")
        self._attr_name = config.get(CONF_NAME) + " HotWater consumption"
        self._attr_unique_id = self._attr_name
