import RPi.GPIO as gpio
from time import sleep
from spell_iot import Spell_IoT

DEVICE_TOKEN = "********************"

gpio.setwarnings(False)
rows_p = [29, 31, 33, 35]
cols_p = [37, 40, 38, 26]
key = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

gpio.setmode(gpio.BOARD)

for column in cols_p:
    gpio.setup(column, gpio.OUT)
    gpio.output(column, gpio.HIGH)

for row in rows_p:
    gpio.setup(row, gpio.IN, pull_up_down=gpio.PUD_UP)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    # Start the Spell IoT background thread
    Spell_iot.autoRun()

if __name__ == "__main__":
    setup()
    print("Waiting for key press...")
    
    # Store the last pressed key to prevent spamming messages to Cloud while button is held
    last_key = None
    
    try:
        while True:
            key_pressed_in_this_loop = False
            for i in range(4):
                gpio.output(cols_p[i], gpio.LOW)
                
                for j in range(4):
                    if gpio.input(rows_p[j]) == gpio.LOW:
                        current_key = key[j][i]
                        key_pressed_in_this_loop = True
                        
                        # Only send if it's a new key press
                        if current_key != last_key:
                            print(f"Key Pressed: {current_key}")
                            # Send the pressed key to V6
                            Spell_iot.write("V6", current_key)
                            last_key = current_key
                            sleep(0.2) # Small debounce delay
                            
                gpio.output(cols_p[i], gpio.HIGH)
                
            # If no key is pressed in the entire scan, reset last_key
            if not key_pressed_in_this_loop:
                last_key = None
                
            sleep(0.05)
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        gpio.cleanup()
