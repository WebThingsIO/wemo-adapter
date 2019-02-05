"""Wemo adapter for Mozilla IoT Gateway."""

from gateway_addon import Device
from pywemo.ouimeaux_device.api.service import ActionException
import threading
import time

from .wemo_property import (WemoDimmerProperty, WemoInsightProperty,
                            WemoSwitchProperty)


_POLL_INTERVAL = 5


class WemoDevice(Device):
    """Wemo device type."""

    def __init__(self, adapter, _id, wemo_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        wemo_dev -- the wemo device object to initialize from
        """
        Device.__init__(self, adapter, _id)
        self._type = []

        self.wemo_dev = wemo_dev
        self.description = wemo_dev.model
        self.name = wemo_dev.name

        self.wemo_dev.update_binary_state()

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()


class WemoSwitch(WemoDevice):
    """Wemo switch type."""

    def __init__(self, adapter, _id, wemo_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        wemo_dev -- the wemo device object to initialize from
        """
        WemoDevice.__init__(self, adapter, _id, wemo_dev)

        self._type = ['OnOffSwitch']
        self.type = 'onOffSwitch'

        self.properties['on'] = WemoSwitchProperty(
            self,
            'on',
            {
                '@type': 'OnOffProperty',
                'label': 'On/Off',
                'type': 'boolean',
            },
            self.is_on())

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)

            try:
                self.wemo_dev.update_binary_state()
            except ActionException:
                continue

            for prop in self.properties.values():
                prop.update()

    def is_on(self):
        """Determine whether or not the switch is on."""
        try:
            state = int(self.wemo_dev.basic_state_params.get('BinaryState', 0))
            return state != 0
        except (ValueError, AttributeError):
            return False


class WemoInsight(WemoSwitch):
    """Wemo Insight smart plug type."""

    def __init__(self, adapter, _id, wemo_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        wemo_dev -- the wemo device object to initialize from
        """
        WemoSwitch.__init__(self, adapter, _id, wemo_dev)
        self.wemo_dev.update_insight_params()

        self._type.extend(['SmartPlug', 'EnergyMonitor'])
        self.type = 'smartPlug'

        self.properties['instantaneousPower'] = WemoInsightProperty(
            self,
            'instantaneousPower',
            {
                '@type': 'InstantaneousPowerProperty',
                'label': 'Power',
                'type': 'number',
                'unit': 'watt',
            },
            self.wemo_dev.current_power / 1000)

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)

            try:
                self.wemo_dev.update_binary_state()
                self.wemo_dev.update_insight_params()
            except ActionException:
                continue

            for prop in self.properties.values():
                prop.update()

    def power(self):
        """Determine the current power usage, in watts."""
        return self.wemo_dev.current_power / 1000


class WemoDimmer(WemoSwitch):
    """Wemo dimmer type."""

    def __init__(self, adapter, _id, wemo_dev):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        wemo_dev -- the wemo device object to initialize from
        """
        WemoSwitch.__init__(self, adapter, _id, wemo_dev)
        self.wemo_dev.get_brightness(force_update=True)

        self._type.append('MultiLevelSwitch')
        self.type = 'multiLevelSwitch'

        self.properties['level'] = WemoDimmerProperty(
            self,
            'level',
            {
                '@type': 'LevelProperty',
                'label': 'Level',
                'type': 'number',
                'unit': 'percent',
                'minimum': 0,
                'maximum': 100,
            },
            self.level())

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)

            try:
                self.wemo_dev.update_binary_state()
                self.wemo_dev.get_brightness(force_update=True)
            except ActionException:
                continue

            for prop in self.properties.values():
                prop.update()

    def level(self):
        """Determine the current level."""
        return self.wemo_dev.get_brightness()
