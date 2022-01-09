"""BAXI thermostat's constant """
from homeassistant.components.climate.const import HVAC_MODE_AUTO, HVAC_MODE_OFF

# Generic
VERSION = "1.0"
DOMAIN = "baxi_thermostat"
PLATFORM = "climate"
ISSUE_URL = "https://github.com/vipial1/BAXI_thermostat"

STORAGE_VERSION = 1
STORAGE_KEY = "baxiapi"

# Defaults
DEFAULT_NAME = "Baxi Thermostat"
DEVICE_MODEL = "TXM 10C"
DEVICE_MANUFACTER = "Baxi"

PRESET_MODE_MANUAL = "Manual"
PRESET_MODE_SCHEDULE_1 = "Schedule 1"
PRESET_MODE_SCHEDULE_2 = "Schedule 2"
PRESET_MODE_SCHEDULE_3 = "Schedule 3"
PRESET_MODE_TEMP_OVERRIDE = "Temporary Override"
PRESET_MODE_ANTIFROST = "Anti Frost"

PRESET_MODES = [
    PRESET_MODE_MANUAL,
    PRESET_MODE_SCHEDULE_1,
    PRESET_MODE_SCHEDULE_2,
    PRESET_MODE_SCHEDULE_3,
    PRESET_MODE_TEMP_OVERRIDE,
    PRESET_MODE_ANTIFROST,
]

HVAC_MODES = [HVAC_MODE_OFF, HVAC_MODE_AUTO]
