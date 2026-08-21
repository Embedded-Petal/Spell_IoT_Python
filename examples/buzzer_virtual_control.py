import time
import RPi.GPIO as GPIO

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "***********"

BUZZER_PIN = 26

# Set up GPIO mode (BCM mode is standard for Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

# Define the callback function for V9
def v9_callback(value):
    try:
        buzzer_state = int(value)
        if buzzer_state == 1:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            print("Buzzer turned ON!")
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            print("Buzzer turned OFF!")
    except ValueError:
        pass

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Register the pin (V9) with our callback
    Spell_iot.registerPin("V9", v9_callback)
    
    # Start the background loop for the web socket
    Spell_iot.loop_start()

def loop():
    print("Program running... Waiting for V9 virtual control!")
    while True:
        # Small delay to prevent 100% CPU usage
        time.sleep(0.1)

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nExiting Program")
        GPIO.cleanup()
