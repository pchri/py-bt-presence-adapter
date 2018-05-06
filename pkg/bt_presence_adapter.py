"""Bluetooth Presence Detector adapter for Mozilla IoT Gateway."""

from gateway_addon import Adapter, Database
from .bt_presence_device import BluetoothPresenceDevice

import bluetooth as bt

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
        for d in config['devices']:
            self.create_device(d['name'], d['addr'], d['type'])

    def create_device(self, name, addr, type):
        device = None
        if type == _BLUETOOTH_TYPE:
            device = BluetoothPresenceDevice(self, addr, addr, name)
        elif type == _BLE_TYPE:
            device = BluetoothPresenceDevice(self, addr, addr, name)
        if device:
            self.handle_device_added(device)

    def save_config(self):
        db = Database(self.get_package_name())
        db.open()
        config = db.save_config(self.config)
        db.close()

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        self.pairing = True
        config_chanced = False
        for addr, name in bt.discover_devices(duration=min(timeout, _TIMEOUT), flush_cache=True, lookup_names=True):
            if not self.pairing:
                break
            if addr not in self.devices:
                d = { 'name': name, 'addr': addr, 'type': _BLUETOOTH_TYPE }
                self.config['devices'].append(d)
                config_changed = True
                self.create_device(name, addr, _BLUETOOTH_TYPE)
        if config_changed:
            self.save_config()

        self.pairing = False


    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
