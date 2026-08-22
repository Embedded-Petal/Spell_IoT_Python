'''
pip3 install adafruit-circuitpython-charlcd
'''
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from spell_iot import Spell_IoT

DEVICE_TOKEN = "********************"

lcd_columns = 16
lcd_rows = 2

# led = digitalio.DigitalInOut(board.D13)
# led.direction = digitalio.Direction.OUTPUT

lcd_rs = digitalio.DigitalInOut(board.D12)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D16)
lcd_d7 = digitalio.DigitalInOut(board.D18)

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.cursor = False
lcd.clear()
lcd.message = "Welcome to Petal"

Spell_iot = Spell_IoT()

# Variable to hold the current message
current_msg = "Welcome to Petal"

def v6_callback(value):
    global current_msg
    print(f"Received on V6: {value}")
    current_msg = str(value)
    
    # Clear the LCD and update with the new message
    lcd.clear()
    lcd.message = current_msg

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Register callback for pin V6
    Spell_iot.registerPin("V6", v6_callback)
    
    # Start the Spell IoT background thread
    Spell_iot.autoRun()

if __name__ == "__main__":
    setup()
    print("Waiting for messages on V6...")
    time.sleep(2)
    
    try:
        while True:
            # Scroll the message left only if it's longer than the LCD width
            if len(current_msg) > lcd_columns:
                lcd.move_left()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
        lcd.clear()
