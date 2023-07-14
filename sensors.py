import spidev
import board
import busio
import adafruit_ina219
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import digitalio
import adafruit_max31856
import time
import random

# INA219DC setup
i2c_bus = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c_bus)

# ADS1115 setup
ads = ADS.ADS1115(i2c_bus)
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

# ACS758LCB setup
spi = spidev.SpiDev()
spi.open(0,0)

def read_ina219():
    return "{:.3f}".format(ina219.current)

def read_ads1115():
    return "{:.3f}".format(chan0.voltage), "{:.3f}".format(chan1.voltage)

def read_acs758lcb():
    def read_channel(channel):
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    acs758lcb_data = read_channel(0)
    return "{:.3f}".format(acs758lcb_data)

def read_max31856():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)  # Set to appropriate chip select for your wiring
    sensor = adafruit_max31856.MAX31856(spi, cs)
    return "{:.3f}".format(sensor.temperature)

# RGB LED setup
RED_LED_PIN = 17
GREEN_LED_PIN = 27
BLUE_LED_PIN = 22

# Set up the GPIO pins as outputs
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

# Set up the GPIO pins for PWM
red_pwm = GPIO.PWM(RED_LED_PIN, 100)  # 100 Hz frequency
green_pwm = GPIO.PWM(GREEN_LED_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_LED_PIN, 100)

# Start the PWM outputs with a duty cycle of 0 (off)
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

# Global variables to store the duty cycle
red_duty_cycle = 0
green_duty_cycle = 0
blue_duty_cycle = 0

# Set up the GPIO pins for the button and relay
BUTTON_PIN = 20
RELAY_PIN = 26

# Set up the button and relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def read_button():
    return GPIO.input(BUTTON_PIN)

def read_relay():
    return GPIO.input(RELAY_PIN)

def toggle_relay():
    GPIO.output(RELAY_PIN, not GPIO.input(RELAY_PIN))

# Define a dictionary to map RGB values to color names
color_names = {
    (100, 0, 0): 'Red',
    (100, 100, 0): 'Yellow',
    (0, 100, 0): 'Green',
    (0, 100, 100): 'Cyan',
    (0, 0, 100): 'Blue',
    (100, 0, 100): 'Magenta'
}

def get_random_color():
    # Generate a random color
    color = random.choice(list(color_names.keys()))
    return color

def get_color_name(color):
    # Get the name of the color
    return color_names.get(color, 'Unknown')

def handle_button_press(channel):
    # Get a random color
    color = get_random_color()
    # Set the LED to the random color
    set_led_color(color)
    # Print the name of the color
    print(f'LED color: {get_color_name(color)}')

def set_led_color(color):
    # Convert the color to a percentage for PWM
    red, green, blue = [c for c in color]  # Adjusted calculation

    # Change the duty cycle of the PWM to change the color
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

    # Update the global duty cycle variables
    global red_duty_cycle, green_duty_cycle, blue_duty_cycle
    red_duty_cycle, green_duty_cycle, blue_duty_cycle = red, green, blue

def read_led_color():
    # Convert the duty cycle back to a color value
    color = (red_duty_cycle / 100.0 * 255, green_duty_cycle / 100.0 * 255, blue_duty_cycle / 100.0 * 255)

    return color

# Set up an interrupt to detect when the button is pressed
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=handle_button_press, bouncetime=200)

# Add the change_led_color function
def change_led_color():
    # Get a random color
    color = get_random_color()
    # Set the LED to the random color
    set_led_color(color)
