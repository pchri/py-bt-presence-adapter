"""Bluetooth Presence Detector adapter for Mozilla IoT Gateway."""

from gateway_addon import Device
import threading
import sys, time

from .bt_presence_property import BluetoothPresenceProperty

import bluetooth.bluez as bt

_POLL_INTERVAL = 10

class BluetoothPresenceDevice(Device):
    """Bluetooth Presence Detector device type."""

    def __init__(self, adapter, _id, addr, name):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        addr -- the BT address to detect
        name -- name of the BT device with the addr
        """
        Device.__init__(self, adapter, _id)

        self.addr = addr
        self.name = name
        self.type = 'binarySensor'
        self.properties['on'] = BluetoothPresenceProperty(self, False)

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            if not self.adapter.pairing:
                res = bt.lookup_name(self.addr)
                bval = not not res
                self.properties['on'].update(bval)
