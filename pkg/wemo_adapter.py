"""Wemo adapter for Mozilla IoT Gateway."""

from gateway_addon import Adapter
from pywemo import discover_devices, Insight, LightSwitch, Dimmer, Switch

from .wemo_device import WemoDimmer, WemoInsight, WemoSwitch


_TIMEOUT = 3


class WemoAdapter(Adapter):
    """Adapter for Wemo smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'wemo-adapter',
                         'wemo-adapter',
                         verbose=verbose)

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        self.pairing = True
        for dev in discover_devices():
            if not self.pairing:
                break

            _id = 'wemo-' + dev.serialnumber
            if _id not in self.devices:
                if isinstance(dev, Insight):
                    device = WemoInsight(self, _id, dev)
                elif isinstance(dev, LightSwitch) or \
                        isinstance(dev, Switch):
                    device = WemoSwitch(self, _id, dev)
                elif isinstance(dev, Dimmer):
                    device = WemoDimmer(self, _id, dev)
                else:
                    continue

                self.handle_device_added(device)

        self.pairing = False

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
