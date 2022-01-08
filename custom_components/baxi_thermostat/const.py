"""BAXI thermostat's constant """
from homeassistant.components.climate.const import HVAC_MODE_HEAT

# Generic
VERSION = "1.0"
DOMAIN = "baxi_thermostat"
PLATFORM = "climate"
ISSUE_URL = "https://github.com/vipial1/BAXI_thermostat"

STORAGE_VERSION = 1
STORAGE_KEY = "baxiapi"

# Defaults
DEFAULT_NAME = "Baxi Thermostat"

PRESET_MODE_MANUAL = "Manual"
PRESET_MODE_SCHEDULE = "Schedule"

PRESET_MODES = [
    PRESET_MODE_MANUAL,
    PRESET_MODE_SCHEDULE,
]

HVAC_MODES = [HVAC_MODE_HEAT]
