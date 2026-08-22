import time
import RPi.GPIO as GPIO

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "***********"

TRIG_PIN = 23
ECHO_PIN = 24

# Set up GPIO mode (BCM mode is standard for Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    
    distance = pulse_duration * 34300 / 2
    
    # Prints the distance in the terminal & Cloud
    print(f"Distance (cm): {distance:.2f}")
    
    # Send distance to V6 (rounded to 2 decimal places)
    Spell_iot.write("V6", round(distance, 2))

def setup():
    # Connect using the device token
    Spell_iot.begin(DEVICE_TOKEN)
    
    # Start the background loop for the web socket
    Spell_iot.loop_start()

def loop():
    print("Program running... Reading Ultrasonic Sensor!")
    # Let the sensor settle first
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(2)
    
    while True:
        distance()
        time.sleep(1) # 1000ms delay just like the Arduino code

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nExiting Program")
        GPIO.cleanup()
