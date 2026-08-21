import time
import RPi.GPIO as GPIO

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "*******************"
BUTTON_PIN = 16

# Set up GPIO mode (BCM mode is standard for Raspberry Pi)
GPIO.setmode(GPIO.BCM)
one_time = 1
# Set pin 16 as an INPUT pin. 
# We use pull_up_down=GPIO.PUD_DOWN to keep the pin LOW when not pressed.
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Start the background loop for the web socket
    Spell_iot.loop_start()

def loop():
    print("Program running... Press the button!")
    while True:
        # Read the button state (1 / HIGH when pressed)
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH and one_time == 1:
            # Send '1' to Pin 'V4'
            Spell_iot.write("V0", 1)
            one_time = 0
            # Add a short delay to prevent flooding the server 
            # with thousands of messages per second while holding the button.
            time.sleep(0.3)
        elif GPIO.input(BUTTON_PIN) == GPIO.LOW and one_time == 0:
            Spell_iot.write("V0",0)
        # Small delay to prevent 100% CPU usage
        time.sleep(0.1)

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nExiting Program")
        GPIO.cleanup()
