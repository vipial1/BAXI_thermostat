# BAXI THERMOSTAT
This component provides integration with Baxi branded thermostat (**ONLY TESTED WITH [TXM](https://www.baxi.es/productos/termostatos-regulacion/baxi-connect/baxi-connect)**)
## HOW TO INSTALL
It is planned to enable HACS integration soon. Until then, please, copy `baxi_thermostat` into your `custom_components` folder

## CONFIGURATION
Only manual setup is available right now
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

## SCREENSHOT
Integration will create a climate entity, that will look like this in Lovelace:
![](https://github.com/vipial1/BAXI_thermostat/blob/main/screenshot.png?raw=true)

Integration will also create a couple of entities for energy consumption


## WORK IN PROGRESS
- Super huge refactor (code is completely shitty now)
- Lots (seriously, lots) of bugs to be fixed.
- Multidevice not tested, probably not working
- Add to HACS

## NOTES
Thanks to [Domaray](https://community.home-assistant.io/u/Domaray) and [ibernat](https://community.home-assistant.io/u/ibernat) for providing most of the API calls
