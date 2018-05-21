"""Bluetooth (BLE) Presence Detector Device for Mozilla IoT Gateway."""

from gateway_addon import Device
import threading
import sys, time

from .bt_presence_property import BluetoothPresenceProperty
from .ble_interface import BLEDiscover

import functools
print = functools.partial(print, flush=True)

_POLL_INTERVAL = 10
_POLL_TIMEOUT = 10

class BLEPresenceDevice(Device):
    """Bluetooth (BLE) Presence Detector device type."""

    scanner = None
    adapter = None

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

        if not BLEPresenceDevice.scanner:
            BLEPresenceDevice.adapter = adapter
            BLEPresenceDevice.scanner = threading.Thread(target=BLEPresenceDevice.poll)
            BLEPresenceDevice.scanner.daemon = True
            BLEPresenceDevice.scanner.start()

    @staticmethod
    def poll():
        """Poll BLEs for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            if not BLEPresenceDevice.adapter.pairing:
                try:
                    devs = list(BLEDiscover(_POLL_TIMEOUT))
                    for addr, dev in BLEPresenceDevice.adapter.devices.items():
                        if isinstance(dev, BLEPresenceDevice):
                            dev.properties['on'].update(addr in devs)
                except:
                    print("BLE discover exception ", sys.exc_info())
