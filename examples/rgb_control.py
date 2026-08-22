'''
NeoPixel requires sudo to run on Raspberry Pi.
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel --break-system-packages
sudo pip3 install spelliot --break-system-packages
sudo python3 rgb_control.py 
'''
import time
import board
import neopixel
from spell_iot import Spell_IoT

DEVICE_TOKEN = "********************"

# Initialize 8 NeoPixels on GPIO 18 (board.D18)
NUM_PIXELS = 8
pixels1 = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=1)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def v5_callback(value):
    # Spell_IoT library automatically converts the received HEX string to an RGB tuple
    r, g, b = Spell_iot.readRGB("V5")
    
    print(f"Received Color: {value} -> RGB({r}, {g}, {b})")
    
    # Set the color to all pixels
    pixels1.fill((r, g, b))

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Register callback for pin V5
    Spell_iot.registerPin("V5", v5_callback)
    
    # Start the Spell IoT background thread
    Spell_iot.autoRun()

if __name__ == "__main__":
    setup()
    print("Waiting for RGB color data on V5...")
    
    try:
        while True:
            # Main thread can sleep while background thread handles WebSocket
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        # Turn off LEDs on exit
        pixels1.fill((0, 0, 0))
