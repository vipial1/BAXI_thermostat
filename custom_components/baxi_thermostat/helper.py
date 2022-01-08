from .const import PRESET_MODE_MANUAL, PRESET_MODE_SCHEDULE


def convert_preset_mode(raw_mode):
    if raw_mode == "schedule":
        return PRESET_MODE_SCHEDULE
    elif raw_mode == "manual":
        return PRESET_MODE_MANUAL
