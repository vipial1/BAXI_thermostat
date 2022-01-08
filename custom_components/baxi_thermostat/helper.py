from .const import (
    PRESET_MODE_MANUAL,
    PRESET_MODE_SCHEDULE_1,
    PRESET_MODE_SCHEDULE_2,
    PRESET_MODE_SCHEDULE_3,
    PRESET_MODE_TEMP_OVERRIDE,
    PRESET_MODE_ANTIFROST,
)
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    HVAC_MODE_AUTO,
)


def convert_preset_mode(raw_mode, program=None):

    if raw_mode == "manual":
        return PRESET_MODE_MANUAL
    elif raw_mode == "temporary-override":
        return PRESET_MODE_TEMP_OVERRIDE
    elif raw_mode == "anti-frost":
        return PRESET_MODE_ANTIFROST
    elif raw_mode == "schedule" and program == 1:
        return PRESET_MODE_SCHEDULE_1
    elif raw_mode == "schedule" and program == 2:
        return PRESET_MODE_SCHEDULE_2
    elif raw_mode == "schedule" and program == 3:
        return PRESET_MODE_SCHEDULE_3


def convert_hvac_mode(raw_mode):
    if raw_mode == "off":
        return HVAC_MODE_OFF
    elif raw_mode == "heating-auto":
        return HVAC_MODE_AUTO
