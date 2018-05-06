"""Bluetooth Presence Detection adapter for Mozilla IoT Gateway."""

from gateway_addon import Property

class BluetoothPresenceProperty(Property):
    """Bluetooth Presence property type."""

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

    def update(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)

