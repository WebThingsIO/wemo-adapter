"""Wemo adapter for Mozilla IoT Gateway."""

from gateway_addon import Property


class WemoProperty(Property):
    """Wemo property type."""

    def __init__(self, device, name, description, value):
        """
        Initialize the object.

        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        Property.__init__(self, device, name, description)
        self.set_cached_value(value)


class WemoSwitchProperty(WemoProperty):
    """Property type for Wemo switches."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name != 'on':
            return

        self.device.wemo_dev.set_state(value)
        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        if self.name != 'on':
            return

        value = self.device.is_on()

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


class WemoInsightProperty(WemoProperty):
    """Property type for Wemo Insight smart plugs."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        return

    def update(self):
        """Update the current value, if necessary."""
        if self.name != 'instantaneousPower':
            return

        value = self.device.power()

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


class WemoDimmerProperty(WemoProperty):
    """Property type for Wemo dimmers."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name != 'level':
            return

        self.device.wemo_dev.set_brightness(value)
        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        if self.name != 'level':
            return

        value = self.device.level()

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
