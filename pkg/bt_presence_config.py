"""Bluetooth Presence Detector configuration for Mozilla IoT Gateway."""

from gateway_addon import Database

class BluetoothPresenceConfig:
    """Configuration data for BluetoothPresenceAdapter."""

    def __init__(self, package_name):
        self.package_name = package_name
        self.load()

    def load(self):
        self.config_changed = False
        db = Database(self.package_name)
        db.open()
        self.config = db.load_config()
        db.close()

    def save(self):
        if self.config_changed:
            self.config_changed = False
            db = Database(self.package_name)
            db.open()
            db.save_config(self.config)
            db.close()

    def configured_devices(self):
        return self.config['devices']

    def add_device_configuration(self, addr, name, type):
        if addr not in map(lambda o: o['addr'], self.config['devices']):
            d = { 'name': name, 'addr': addr, 'type': type }
            self.config['devices'].append(d)
            self.config_changed = True
    
    def remove_device_configuration(self, addr):
        for d in self.config['devices']:
            if d['addr'] == addr:
                self.config['devices'].remove(d)
                self.config_changed = True
                self.save()
                break
