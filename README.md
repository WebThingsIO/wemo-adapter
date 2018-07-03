# wemo-adapter

Wemo device adapter for Mozilla IoT Gateway.

# Supported Devices

## Tested and Working

* Smart plugs
    * Mini Smart Plug

## Untested but _Should Work_

* Insight Smart Plug
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
sudo apt install python3-dev libnanomsg-dev
sudo pip3 install nnpy
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
