# wemo-adapter

Wemo device adapter for WebThings Gateway.

# Supported Devices

## Tested and Working

* Smart plugs
    * Mini Smart Plug
    * Insight Smart Plug

## Untested but _Should Work_

* Light Switch
* Dimmer

# Unsupported Devices

There's nothing technically preventing support for these devices, they just have not been tested at all.

* Bridge
* Light bulbs
* Slow cooker
* Maker
* Heater
* Air purifier
* Humidifier
* Coffee maker

# Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo pip3 install git+https://github.com/WebThingsIO/gateway-addon-python.git
```
