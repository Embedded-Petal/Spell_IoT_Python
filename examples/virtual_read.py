import time
import RPi.GPIO as GPIO

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "*******************"

LED1 = 13
LEDState1 = 0

# Set up GPIO mode (BCM mode is standard for Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.output(LED1, GPIO.LOW)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

# Define the callback function for V0
def v0_callback(value):
    global LEDState1
    try:
        LEDState1 = int(value)
    except ValueError:
        pass

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Register the pin (V0) with our callback
    Spell_iot.registerPin("V0", v0_callback)
    
    # Start the background loop for the web socket
    Spell_iot.loop_start()

def loop():
    while True:
        # In Python, we control the LED inside the loop based on LEDState1
        if LEDState1 == 1:
            GPIO.output(LED1, GPIO.HIGH)
        else:
            GPIO.output(LED1, GPIO.LOW)
            
        time.sleep(0.1) # Small delay to prevent 100% CPU usage

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nExiting Program")
        GPIO.cleanup()
