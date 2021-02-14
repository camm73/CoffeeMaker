from coffee_api import CoffeeAPI
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Start IoT Coffee Maker")
    api = CoffeeAPI()
    api.start(blocking=True)
