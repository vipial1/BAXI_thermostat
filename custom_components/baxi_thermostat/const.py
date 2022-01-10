"""BAXI thermostat's constant """
from homeassistant.components.climate.const import HVAC_MODE_AUTO, HVAC_MODE_OFF

# Generic

VERSION = "1.0"
DOMAIN = "climate"
PLATFORM = "baxi_thermostat"
ISSUE_URL = "https://github.com/vipial1/BAXI_thermostat"

STORAGE_VERSION = 1
STORAGE_KEY = "baxiapi"

DATA_KEY_API = "api"
DAYA_KEY_CONFIG = "config"

# Defaults
DEFAULT_NAME = "Baxi Thermostat"
DEVICE_MODEL = "TXM"
DEVICE_MANUFACTER = "Baxi"

BAXI_PRESET_MANUAL = "manual"
BAXI_PRESET_SCHEDULE = "schedule"
PRESET_MODE_MANUAL = "Manual"
PRESET_MODE_SCHEDULE_1 = "Schedule 1"
PRESET_MODE_SCHEDULE_2 = "Schedule 2"
PRESET_MODE_SCHEDULE_3 = "Schedule 3"
PRESET_MODE_TEMP_OVERRIDE = "Temporary Override"
PRESET_MODE_ANTIFROST = "Anti Frost"
PRESET_MODE_HOLIDAY = "Holidays"

PRESET_MODES = [
    PRESET_MODE_MANUAL,
    PRESET_MODE_SCHEDULE_1,
    PRESET_MODE_SCHEDULE_2,
    PRESET_MODE_SCHEDULE_3,
    PRESET_MODE_TEMP_OVERRIDE,
    PRESET_MODE_ANTIFROST,
    PRESET_MODE_HOLIDAY,
]

HVAC_MODES = [HVAC_MODE_OFF, HVAC_MODE_AUTO]
