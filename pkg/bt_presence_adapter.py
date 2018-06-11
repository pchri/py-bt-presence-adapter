"""Bluetooth Presence Detector adapter for Mozilla IoT Gateway."""

import threading

from gateway_addon import Adapter
from .bt_presence_device import BluetoothPresenceDevice
from .ble_presence_device import BLEPresenceDevice
from .ble_interface import BLEDiscover
from .bt_interface import BTDiscover

import functools
print = functools.partial(print, flush=True)

_TIMEOUT = 10
_BLUETOOTH_TYPE = "bluetooth"
_BLE_TYPE = "ble"

class BluetoothPresenceAdapter(Adapter):
    """Adapter for BluetoothPresence devices."""

    def __init__(self, config, verbose=False):
        """
        Initialize the object.

        config -- current user configuration
        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'bt-presence-adapter',
                         'bt-presence-adapter',
                         verbose=verbose)

        self.pairing = False
        self.config = config
        for d in self.configured_devices():
            self.create_device(d['name'], d['addr'], d['type'])

    def create_device(self, name, addr, type):
        device = None
        if type == _BLUETOOTH_TYPE:
            device = BluetoothPresenceDevice(self, addr, addr, name)
        elif type == _BLE_TYPE:
            pass
            device = BLEPresenceDevice(self, addr, addr, name)
        if device:
            self.handle_device_added(device)

    def configured_devices(self):
        return self.config.configured_devices()

    def add_device_config(self, addr, name, type):
        self.config.add_device_configuration(addr, name, type)

    def remove_device_config(self, addr):
        self.config.remove_device_configuration(addr)

    def save_config(self):
        self.config.save()

    def ble_pairing(self):
        try:
            for addr, name in BLEDiscover(self.timeout).items():
                if not self.pairing:
                    break
                self.maybe_add(addr, name, _BLE_TYPE)
        except:
            print("BLE discover exception ", sys.exc_info())

    def bt_pairing(self):
        for addr, name in BTDiscover(self.timeout):
            if not self.pairing:
                break
            self.maybe_add(addr, name, _BLUETOOTH_TYPE)

    def maybe_add(self, addr, name, type):
        if addr not in self.devices:
            self.add_device_config(addr, name, type)
            self.create_device(name, addr, type)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        self.pairing = True
        self.timeout = min(timeout, _TIMEOUT)
        t1 = threading.Thread(target=self.bt_pairing)
        t1.start()
        t2 = threading.Thread(target=self.ble_pairing)
        t2.start()
        t1.join()
        t2.join()
        self.save_config()
        self.pairing = False

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False

    def handle_device_removed(self, device):
        addr = device.addr
        super(BluetoothPresenceAdapter, self).handle_device_removed(device)
        self.remove_device_config(addr)
