# bt-presence-adapter
Mozilla IoT adapter for detecting Bluetooth device presence

Exposes individual Bluetooth devices as simple binary sensors. If the Bluetooth device in within range of the IOT gateway the binary sensor will be On, otherwise it will be Off. 

This has many applications. Like automatically turning the IoT enabled toaster off when you leave you house with your phone. Or turning dimmed lights on when you return to your house in the evening.

## Status of version 0.0.0

- Can scan for standard bluetooth (and BLE) devices
- Creates device configuration for each detected device
- Device configuration exposed and visible in the add-ons GUI
- Real-time (well - scanning every 10 seconds) presence of device as a binary sensor
- Gracefully (and silently) handles missing Bluetooth/BLE python modules

Tested on my RPi 3. It can detect my iPhone, iPad, Linux laptop, Windows laptop, an Adafruit Bluefruit LE device and a Garmin Forerunner 235.

## TODO

- ~~Figure out how to detect BLE devices without being root. The standard tools can detect my Adafruit Bluefruit LE and my Garmin Forerunner only when running as root. The Python library also requires root priviledges.~~
- ~~Need to move configuration handling to a separate class~~
- ~~Implement the BLEDevice class. Probably using a class/static thread variable~~
- ~~Figure out the dependencies/requirements.txt ~~
- ~~Test what happens when other processes are using BT. It seems the exception handling in the BLE code does the trick.~~
- Make a release

## Install on top of a Mozilla prebuilt Raspberry Pi OS image

To get standard Bluetooth to work this should be done before enabling the adapter

```
% sudo apt-get install libbluetooth-dev
% sudo pip3 install pybluez
```

To get BLE to work this should be done in addition to the above before enabling the adapter

```
% sudo apt-get install libglib2.0-dev libboost-python-dev libboost-thread-dev
% sudo pip3 install pygattlib
% sudo setcap cap_net_raw,cap_net_admin+eip `readlink -f \`which python3\``
```

## Installing on gateway you've installed from sources
(Incomplete - don't try this at home - it may kill your hamster)

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

