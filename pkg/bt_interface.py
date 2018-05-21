"""BT interface."""

import functools
print = functools.partial(print, flush=True)

hasBT = False

try:
    import bluetooth as bt
    import bluetooth.bluez as bluez
    hasBT = True
except:
    print("BT not available")

def BTDiscover(timeout):
    if hasBT:
        return bt.discover_devices(timeout, flush_cache=True, lookup_names=True)
    return {}

def BTLookupName(addr):
    if hasBT:
        return bluez.lookup_name(addr)
    return False