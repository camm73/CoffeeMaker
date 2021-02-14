from flask_api import flask_api, status
from coffee_controller import CoffeeController
import threading
import logging

app = FlaskAPI(__name__)
controller = CoffeeController()

@app.route('/turn-on', methods=['POST'])
def turn_on():
    controller.turn_on()

@app.route('/turn-off', methods=['POST'])
def turn_off():
    controller.turn_off()

@app.route('/make-coffee', methods=['POST'])
def make_coffee():
    runtime_minutes = request.data.get('minutes', None)
    if runtime_minutes is None:
        return {
            'message': "'minutes' field must be included with request"
        }, status.HTTP_400_BAD_REQUEST

# Blocking request to start API
def start_API():
    while True:
        try:
            app.run(debug=False, host='0.0.0.0')
        except Exception as e:
            logging.error(f"API crashed: {e}")
