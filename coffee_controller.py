import RPi.GPIO as gpio
import time
import logging
import atexit
import threading

logging.basicConfig(level=logging.INFO)

class CoffeeController():
    def __init__(self, control_pin: int = 4):
        self.CONTROL_PIN = control_pin
        self._on = False
        self._long_run_thread = None

        # Setup gpio pins before use
        self.configure_gpio()

    # Configures control pin as output
    def configure_gpio(self) -> None:
        logging.info("Configuring GPIO pins")
        gpio.setmode(gpio.BCM)
        gpio.setup(self.CONTROL_PIN, gpio.OUT)
        gpio.output(self.CONTROL_PIN, gpio.LOW)
        
        # Make sure cleanup is called at exit
        atexit.register(self.cleanup)

    # Active high control of relay
    def turn_on(self) -> None:
        logging.info(f"Turning on coffee maker at: {time.time()}")
        gpio.output(self.CONTROL_PIN, gpio.HIGH)
        self._on = True

    # Active low to disable relay
    def turn_off(self) -> None:
        logging.info(f"Turning off coffee maker at {time.time()}")
        gpio.output(self.CONTROL_PIN, gpio.LOW)
        self._on = False

    # Non-blocking method to start coffee for designated time period
    def start_coffee(self, minutes: int = 60):
        self._long_run_thread = threading.Thread(target=self._long_run_coffee, args=(minutes,))
        self._long_run_thread.start()

    # Handles making coffee for a long duration
    def _long_run_coffee(self, minutes: int) -> None:
        self.turn_on()
        time.sleep(minutes * 60)
        self.turn_off()

    # Check whether coffee maker is on
    def is_on(self) -> bool:
        return self._on

    # Makes sure all gpios are cleaned up before exit
    def cleanup(self) -> None:
        self.turn_off()
        logging.info("Cleaning up GPIO pins")
        gpio.cleanup()
