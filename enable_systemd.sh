#!/bin/bash

echo "Setting up systemd service for coffee pi..."
# Copy systemd service into place
sudo cp coffee_pi.service /etc/systemd/system/coffee_pi.service

# Enable service
sudo systemctl enable coffee_pi.service

# Start service
sudo systemctl start coffee_pi.service

echo "Successfully setup systemd for coffee pi!"