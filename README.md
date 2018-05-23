# bt-presence-adapter
Mozilla IoT adapter for detecting Bluetooth device presence

Exposes individual Bluetooth devices as simple binary sensors

## Status of version 0.0.0

- Can scan for standard bluetooth (and BLE) devices
- Creates device configuration for each detected device
- Device configuration exposed and visible in the add-ons GUI
- Real-time (well - scanning every 10 seconds) presence of device as a binary sensor
- Gracefully handles missing Bluetooth/BLE python modules

Tested on my RPi 3. It can detect my iPhone, iPad and Linux laptop.

## TODO

- ~~Figure out how to detect BLE devices without being root. The standard tools can detect my Adafruit Bluefruit LE and my Garmin Forerunner only when running as root. The Python library also requires root priviledges.~~
- ~~Need to move configuration handling to a separate class~~
- ~~Implement the BLEDevice class. Probably using a class/static thread variable~~
- Figure out the dependencies/requirements.txt 
- Test what happens when other processes are using BT. It seems the exception handling in the BLE code does the trick.

## Installing

Install ffi library
```
% sudo apt-get install libffi-dev
% sudo apt-get install libnanomsg-dev
```

Install the gateway-addon-python: https://github.com/mozilla-iot/gateway-addon-python

```
git clone https://github.com/mozilla-iot/gateway-addon-python
cd gateway-addon-python
sudo python3 setup.py build
sudo python3 setup.py install
```

The necessary python/bluetooth requirements can be installed like this
```
% sudo apt-get install libcap2-bin python3-pip libbluetooth-dev libglib2.0-dev libboost-thread-dev libboost-python-dev
% sudo python3 -m pip install pybluez pygattlib
% sudo setcap cap_net_raw,cap_net_admin+eip `readlink -f \`which python3\``
```

## INFO

It seems
```
sudo apt-get install libcap2-bin
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/python3.5
```
does the trick...

The capability can be removed again with
```
sudo setcap -r /usr/bin/python3.5
```

Better version 
```
sudo setcap cap_net_raw,cap_net_admin+eip `readlink -f \`which python3\``
```
