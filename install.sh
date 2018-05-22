#!/bin/bash

set -e

sudo apt-get install libcap2-bin libglib2.0-dev libboost-thread-dev libboost-python-dev
sudo python3 -m pip install pygattlib
sudo setcap cap_net_raw,cap_net_admin+eip `readlink -f \`which python3\``