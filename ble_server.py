from bluezero import peripheral
from bluezero import adapter
import logging
import threading
import time
import sys
import re
from controller_utils import set_wifi_network, connect_to_network

# WIFI Service
SERVICE_UUID = 'ed61f1ee-b500-472f-b522-5f7b30177c46'

# Wifi status characteristic
STATUS_CHAR_ID = 'ed61f1ee-b501-472f-b522-5f7b30177c46'
# Wifi data stream characteristic
STREAM_CHAR_ID = 'ed61f1ee-b502-472f-b522-5f7b30177c46'

# STATUS VALUES
READY = 0
INVALID_INPUT = 1
WIFI_ERROR = 2
SUCCESS = 3

class CoffeeWifiSetupServer():
    def __init__(self):
        self._server_thread = None
        self._bluetooth_addr = self._get_bluetooth_addr()
        self._status = READY

        # Confirm that bluetooth address was received
        if self._bluetooth_addr is None:
            raise Exception("Unable to start Coffee Setup Server due to missing bluetooth interface")

    # Retreives address of bluetooth interface
    def _get_bluetooth_addr(self):
        try:
            addr_list = list(adapter.Adapter.available())
            if(len(addr_list)):
                return addr_list[0].address
            else:
                return None
        except Exception as err:
            logging.error(f"Failed to get bluetooth address: {err}")
            return None

    def _status_read_cb(self):
        logging.info(f"Reading status value: {self._status}")
        return [self._status]

    # TODO: To be added in future
    def _status_notify_cb(self, notifying, characteristic):
        pass

    # TODO: Sanitize input before adding to wpa_supplicant.conf
    def _wifi_details_write_cb(self, value, options):
        logging.info(f"Received: {bytes(value).decode('utf-8')}")
        _r = r'ssid\/.*\/pass\/.*'
        results = re.findall(_r, bytes(value).decode('utf-8'))
        if(len(results)):
            wifi_res = results[0].split('/')
            if(wifi_res[0] == 'ssid' and wifi_res[2] == 'pass'):
                ssid = wifi_res[1]
                wifi_pass = wifi_res[3]
                config_status = set_wifi_network(ssid, wifi_pass)
                if not config_status:
                    logging.error(f"Failed to set wifi network")
                    return
                time.sleep(0.5)
                network_status = connect_to_network()

                if not network_status:
                    logging.error(f"Failed to connect to network")
                    self._status = INVALID_INPUT
                    return
                else:
                    logging.info("Successfully connected to network")
                    self._status = SUCCESS
                    sys.exit(0)
        else:
            logging.info("Invalid input received.")
            self._status = INVALID_INPUT

    # Create the BLE Peripheral and configures its services and characteristics
    def run_service(self):
        # Configure Pi's bluetooth interface as BLE Peripheral
        wifi_service = peripheral.Peripheral(self._bluetooth_addr, local_name='Coffee Maker WiFi Setup', appearance=1216)

        # Add service for setting up wifi
        service_id = 1
        wifi_service.add_service(srv_id=service_id, uuid=SERVICE_UUID, primary=True)
        
        # Add chrarateristic for receiving wifi details
        wifi_service.add_characteristic(srv_id=service_id, chr_id=1, uuid=STREAM_CHAR_ID, value=[], notifying=False, flags=['write'], read_callback=None, write_callback=self._wifi_details_write_cb, notify_callback=None)

        # Add characteristic for checking wifi status
        wifi_service.add_characteristic(srv_id=service_id, chr_id=2, uuid=STATUS_CHAR_ID, value=[0x00], notifying=False, flags=['read', 'notify'], read_callback=self._status_read_cb, write_callback=None, notify_callback=self._status_notify_cb)
        
        # Start BLE Peripheral service
        wifi_service.publish()

