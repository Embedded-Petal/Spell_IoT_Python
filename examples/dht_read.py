'''
pip3 install adafruit-circuitpython-dht
'''
import time
import board
import adafruit_dht

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "********************"

# Initialize DHT11 on GPIO 5
# board.D5 represents GPIO 5 (BCM)
dht_device = adafruit_dht.DHT11(board.D5)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def dhtRead():
    try:
        # Read temperature and humidity
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        
        if temperature is not None and humidity is not None:
            print(f"Temp: {temperature}°C | Humidity: {humidity}%")
            Spell_iot.write("V1", temperature)
            Spell_iot.write("V2", humidity)
        else:
            print("Failed to read from DHT11 Sensor!")
            
    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors on Pi, just keep going
        print(f"Failed to read from DHT11 Sensor! ({error.args[0]})")
        time.sleep(2.0)
        return
    except Exception as error:
        dht_device.exit()
        raise error
    
    # Delay 1000ms just like Arduino code
    time.sleep(1)

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Start the background loop for the web socket
    Spell_iot.loop_start()

def loop():
    print("Program running... Reading DHT11 Sensor!")
    # Initial delay for the sensor to stabilize
    time.sleep(2)
    
    while True:
        dhtRead()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nExiting Program")
        dht_device.exit()
