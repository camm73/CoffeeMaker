import RPi.GPIO as gpio
import time
import logging
import atexit

logging.basicConfig(level=logging.INFO)

class CoffeeController():
    def __init__(self, control_pin=4):
        self.CONTROL_PIN = control_pin

        # Setup gpio pins before use
        self.configure_gpio()

    # Configures control pin as output
    def configure_gpio(self):
        logging.info("Configuring GPIO pins")
        gpio.setmode(gpio.BCM)
        gpio.setup(self.CONTROL_PIN, gpio.OUT)
        gpio.output(self.CONTROL_PIN, gpio.HIGH)
        
        # Make sure cleanup is called at exit
        atexit.register(self.cleanup)

    # Active high control of relay
    def turn_on(self):
        logging.info(f"Turning on coffee maker at: {time.time()}")
        gpio.output(self.CONTROL_PIN, gpio.HIGH)

    # Active low to disable relay
    def turn_off(self):
        logging.info(f"Turning off coffee maker at {time.time()}")
        gpio.output(self.CONTROL_PIN, gpio.LOW)

    # TODO: Temporary run configuration; should be non-blocking
    def start_coffee(self, minutes=60):
        self.turn_on()
        time.sleep(minutes * 60)
        self.turn_off()

    # Makes sure all gpios are cleaned up before exit
    def cleanup(self):
        logging.info("Cleaning up GPIO pins")
        gpio.cleanup()

# TODO: REMOVE
if __name__ == "__main__":
    controller = CoffeeController()
    controller.turn_on()
    time.sleep(4)
    controller.turn_off()