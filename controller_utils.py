import logging
import subprocess

logging.basicConfig(level=logging.INFO)
WPA_SUPP_FILE = '/etc/wpa_supplicant/wpa_supplicant.conf'

# Set up Pi's wpa_supplicant.conf file
def set_wifi_network(ssid: str, password: str) -> bool:
    try:
        wpa_conf = (
            "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
            "update_config=1\n"
            "country=US\n"
            "network={\n"
            f" ssid={ssid}\n"
            f" psk={password}\n"
            "}\n"
        )

        # Write configuration to wpa_suppicant.conf file
        with open(WPA_SUPP_FILE, 'w') as wpa_file:
            wpa_file.write(wpa_conf)

        return True
    except Exception as e:
        logging.error(f"Error storing wpa supplicant configuration: {e}")
        return False

# Establish network connection on Pi
def connect_to_network() -> bool:
    try:
        res = subprocess.run(['sudo /sbin/ifconfig wlan0 down && sleep 2 && sudo /sbin/ifconfig wlan0 up'], shell=True, timeout=60)
        if(res.returncode):
            return False
        return True
    except Exception as e:
        logging.error(f"Failed to connect to network: {e}")
        return False


# Check whether Pi is connected to network
def has_internet_connection() -> bool:
    try:
        res = subprocess.run(['/sbin/iwgetid --raw'], timeout=20, text=True, shell=True, capture_output=True)
        if res.returncode:
            logging.error("Error while fetching current network SSID")
            return False
        elif res.stdout is None:
            logging.error("No output captured from SSID fetch")
            return False
        else:
            wifi_network = res.stdout.replace('\n', '')
            if wifi_network == '':
                logging.info("Pi is not connected to a wifi network")
                return False
            else:
                logging.info(f"Pi is connected to: {wifi_network}")
                return True
    except Exception as e:
        logging.error(f"Failed to check if Pi was connected to internet: {e}")
        return False