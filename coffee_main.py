from ble_server import CoffeeWifiSetupServer
from controller_utils import has_internet_connection
from multiprocessing import Process
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting IoT Coffee Maker")
    # Enable bluetooth server for wifi setup if no internet connection
    if not has_internet_connection():
        setup_server = CoffeeWifiSetupServer()
        setup_process = Process(target=setup_server.run_service)
        setup_process.start()
        setup_process.join()
    
    # Start REST API for coffee
    from coffee_api import CoffeeAPI
    api = CoffeeAPI()
    api.start(blocking=True)
