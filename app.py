from flask import Flask, render_template, jsonify
import sensors
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    sensor_readings = {
        'ina219dc': [],
        'ads1115': [],
        'acs758lcb': [],
        'max31856': [],
    }
    timestamps = []
    for _ in range(10):  # Adjust this value to change the number of readings
        sensor_readings['ina219dc'].append(sensors.read_ina219())  # Corrected function call
        sensor_readings['ads1115'].append(sensors.read_ads1115())
        sensor_readings['acs758lcb'].append(sensors.read_acs758lcb())
        sensor_readings['max31856'].append(sensors.read_max31856())
        timestamps.append(datetime.now().strftime('%H:%M:%S'))
    button_state = sensors.read_button()
    relay_state = sensors.read_relay()
    led_color = sensors.get_color_name(sensors.read_led_color())
    return render_template('home.html', sensor_readings=sensor_readings, button_state=button_state, relay_state=relay_state, led_color=led_color, timestamps=timestamps)

@app.route('/toggle', methods=['POST'])
def toggle():
    sensors.toggle_relay()
    sensors.change_led_color()
    return '', 204  # Return a "No Content" response

@app.route('/api/sensor_data')
def get_sensor_data():
    sensor_readings = {
        'ina219dc': sensors.read_ina219(),  # Corrected function call
        'ads1115': sensors.read_ads1115(),
        'acs758lcb': sensors.read_acs758lcb(),
        'max31856': sensors.read_max31856(),
    }
    return jsonify(sensor_readings)

@app.route('/api/device_state')
def get_device_state():
    device_state = {
        'button_state': sensors.read_button(),
        'relay_state': sensors.read_relay(),
        'led_color': sensors.get_color_name(sensors.read_led_color()),
    }
    return jsonify(device_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
