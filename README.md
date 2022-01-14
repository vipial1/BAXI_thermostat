# BAXI THERMOSTAT

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This component provides integration with Baxi branded thermostat (**ONLY TESTED WITH [TXM](https://www.baxi.es/productos/termostatos-regulacion/baxi-connect/baxi-connect)**)
## How to install
You can use HACS to install this integration as custom repository

If you are not using HACS, you must copy `baxi_thermostat` into your `custom_components` folder

## Configuration
Configuration via integration is recommended. Add an instance of `Baxi Thermostat` using the UI:
![](https://github.com/vipial1/BAXI_thermostat/blob/main/images/integration.png?raw=true)

And follow the steps:
![](https://github.com/vipial1/BAXI_thermostat/blob/main/images/configuration.png?raw=true)


Is it also possible to configure manually, but then, only entities will be created (not device).
```yaml
climate:
  - platform: baxi_thermostat
    name: My Baxi Thermostat
    username: <your username>
    password: <your password>
    pairing_code: <your paring code>
```
Pairing code can be get from the thermostat device or from the Baxi app, under:
```Settings > Connected devices and services > Invite someone```

## Screenshot
Integration will create a climate entity, that will look like this in Lovelace:
![](https://github.com/vipial1/BAXI_thermostat/blob/main/images/climate.png?raw=true)

Integration will also create a couple of entities for energy consumption and a Device that groups all entities (only if configured using UI)


## Work in progress
- Super huge refactor (code is completely shitty now)
- Lots (seriously, lots) of bugs to be fixed.
- Multidevice not tested, probably not working
- Translation

## Thanks to
- [Domaray](https://community.home-assistant.io/u/Domaray) and [ibernat](https://community.home-assistant.io/u/ibernat) for providing most of the API calls
