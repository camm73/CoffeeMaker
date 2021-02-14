from flask_api import FlaskAPI, status
from coffee_controller import CoffeeController
import threading
import logging
import time

logging.basicConfig(level=logging.INFO)
app = FlaskAPI(__name__)
controller = CoffeeController()

@app.route('/turn-on', methods=['POST'], strict_slashes=False)
def turn_on():
    try:
        # Attempt to turn on coffee maker
        controller.turn_on()

        return {
            'message': 'Successfully turned on coffee maker'
        }, status.HTTP_200_OK
    except Exception as e:
        logging.error(f"Failed to turn on coffee controller: {e}")

        return {
            'message': f"Failed to turn on coffee controller: {e}"
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/turn-off', methods=['POST'], strict_slashes=False)
def turn_off():
    try:
        # Attempt to turn off coffee maker
        controller.turn_off()

        return {
            'message': 'Successfully turned off coffee maker'
        }, status.HTTP_200_OK
    except Exception as e:
        logging.error(f"Failed to turn off coffee controller: {e}")

        return {
            'message': f"Failed to turn off coffee controller: {e}"
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/make-coffee', methods=['POST'], strict_slashes=False)
def make_coffee():
    # Exract runtime minutes field from the request
    runtime_minutes = str(request.data.get('minutes', None))
    if runtime_minutes is None:
        return {
            'message': "'minutes' field must be included with request"
        }, status.HTTP_400_BAD_REQUEST
    elif not runtime_minutes.isdigit():
        return {
            'message': "'minutes' field must be a number"
        }, status.HTTP_400_BAD_REQUEST
    
    runtime_minutes = int(runtime_minutes)
    
    try:
        # Start coffee maker for specified amount of time
        controller.start_coffee(minutes=runtime_minutes)
        
        return {
            'message': f'Successfully started coffee maker for {runtime_minutes} minutes'
        }, status.HTTP_200_OK
    except Exception as e:
        logging.error(f"Failed to start making coffee: {e}")

        return {
            'message': f"Failed to start making coffee: {e}"
        }, status.HTTP_500_INTERNAL_SERVER_ERROR

class CoffeeAPI():

    def __init__(self):
        self.api_thread = None

    # Internal function for managing api thread
    def _start_api(self, blocking=False):
        self.api_thread = threading.Thread(target=self._run_api, daemon=True)
        self.api_thread.start()
        if blocking:
            self.api_thread.join()


    # Internal function for blocking run of API
    def _run_api(self):
        while True:
            try:
                app.run(debug=False, host='0.0.0.0')
            except Exception as e:
                logging.error(f"API crashed: {e}. Restarting...")
                time.sleep(2)


    # Start up the Coffee Maker's REST API
    def start(self, blocking=False):
        try:
            # Start up API thread
            self._start_api(blocking=blocking)
        except KeyboardInterrupt:
            logging.info("Received keyboard interrupt. Shutting down api")