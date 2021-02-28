import logging

logging.basicConfig(level=logging.INFO)

# Set up Pi's wpa_supplicant.conf file
def set_wifi_network(ssid, password):
    try:
        wpa_conf = (
            "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"
            "update_config=1"
            "country=US"
            "network={"
            f" ssid={ssid}"
            f" psk={password}"
        )

        # Write configuration to wpa_suppicant.conf file
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as wpa_file:
            wpa_file.write(wpa_conf)
    except Exception as e:
        logging.error(f"Error storing wpa supplicant configuration: {e}")
        return False
    
    return True

# Establish network connection on Pi
def connect_to_network():
    pass
