import time
import board
import neopixel
import RPi.GPIO as GPIO

# Import the library we created
from spell_iot import Spell_IoT

DEVICE_TOKEN = "e36ac927593f427c98245423fae4ea251787219674035"

# --- Normal LED Config ---
LED_PIN = 13 # BCM pin 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)


# Initialize the Spell IoT Library object
spell = Spell_IoT()


def on_v0(value):
    """Callback for Normal LED on Pin V0"""
    print(f"Normal LED Callback (V0) -> State: {value}")
    try:
        state = int(value)
        GPIO.output(LED_PIN, GPIO.HIGH if state == 1 else GPIO.LOW)
    except:
        pass



def setup():
    # 1. Start library
    spell.begin(DEVICE_TOKEN)
    
    # 2. Register callbacks (Same as C++ registerPin)
    spell.registerPin("V0", on_v0)
        
    # 3. Start the background thread for WebSockets
    # Similar to xTaskCreate in C++
    spell.loop_start()


if __name__ == "__main__":
    print("Starting Spell IoT Client...")
    setup()
    
    try:
        # Main loop (Same as Arduino loop)
        while True:
            # Send 'Online' status every 10 seconds just like autoRun() does in C++
            spell.writeAck("status", "Online")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("Program stopped.")
        GPIO.cleanup()
