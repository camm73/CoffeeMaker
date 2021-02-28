from coffee_api import CoffeeAPI
from ble_server import CoffeeWifiSetupServer
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Start IoT Coffee Maker")
    setup_server = CoffeeWifiSetupServer()
    setup_server.start_server()
    #api = CoffeeAPI()
    #api.start(blocking=True)
