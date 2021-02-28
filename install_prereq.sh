#!/bin/bash

sudo apt-get update
sudo apt-get install -y bluetooth
sudo apt-get install -y bluez-tools bluez-hcidump
sudo apt-get install libdbus-1-dev libdbus-glib-1-dev
sudo apt-get install -y dbus python-dbus python3-dbus python3-gi

# Install python requirements as admin
sudo python3 -m pip install -r requirements.txt