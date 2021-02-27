from bluezero import peripheral
from bluezero import adapter
import logging
import threading

logging.basicConfig(level=logging.INFO)
# WIFI Service
SERVICE_UUID = 'ed61f1ee-b500-472f-b522-5f7b30177c46'

# Wifi status characteristic
STATUS_CHAR_ID = 'ed61f1ee-b501-472f-b522-5f7b30177c46'
# Wifi data stream characteristic
STREAM_CHAR_ID = 'ed61f1ee-b502-472f-b522-5f7b30177c46'

class CoffeeWifiSetupServer():
    def __init__(self):
        self._server_thread = None
        self._bluetooth_addr = self._get_bluetooth_addr()

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
        # TODO: Replace with check of wifi status
        return [1]

    def _status_notify_cb(self, notifying, characteristic):
        pass

    def _wifi_details_write_cb(self, value):
        print(f"Received: {bytes(value).decode('utf-8')}")

    # Create the BLE Peripheral and configures its services and characteristics
    def _run_service(self, address):
        # Configure Pi's bluetooth interface as BLE Peripheral
        wifi_service = peripheral.Peripheral(address, local_name='Coffee Maker WiFi Setup', appearance=1216)

        # Add service for setting up wifi
        wifi_service.add_service(srv_id=1, uuid=SERVICE_UUID, primary=True)

        # Add characteristic for checking wifi status
        wifi_service.add_characteristic(srv_id=1, chr_id=1, uuid=STATUS_CHAR_ID, value=[0x00],
                                        notifying=False, flags=['read', 'notify'],
                                        read_callback=self._status_read_cb,
                                        write_callback=None,
                                        notify_callback=self._status_notify_cb
                                        )
        
        # Add chrarateristic for receiving wifi details
        wifi_service.add_characteristic(srv_id=1, chr_id=1, uuid=STREAM_CHAR_ID,
                                        value=[], notifying=False,
                                        flags=['write'],
                                        read_callback=None,
                                        write_callback=self._wifi_details_write_cb,
                                        notify_callback=None
                                        )
        # Start BLE Peripheral service
        wifi_service.publish()

    # Starts BLE WiFi setup server
    def start_server(self):
        self._server_thread = threading.Thread(target=self._run_service, args=(self._bluetooth_addr,), daemon=True)
        self._server_thread.start()
        self._server_thread.join()

