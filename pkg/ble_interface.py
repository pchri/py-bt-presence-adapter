"""BLE interface."""

import functools
print = functools.partial(print, flush=True)

hasBLE = False

try:
    from bluetooth.ble import DiscoveryService
    hasBLE = True
except:
    print("BLE not available")

def BLEDiscover(timeout):
    if hasBLE:
        svc = DiscoveryService()
        return svc.discover(timeout)
    return {}
