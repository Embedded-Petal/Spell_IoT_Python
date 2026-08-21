import time
import RPi.GPIO as GPIO

# Import our custom Spell IoT library
from spell_iot import Spell_IoT

DEVICE_TOKEN = "***********"

TRIG_PIN = 4
ECHO_PIN = 15

# Set up GPIO mode (BCM mode is standard for Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialize Spell IoT
Spell_iot = Spell_IoT()

def distance():
    # Send a 10-microsecond pulse to the TRIG pin
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.000002) # 2 microseconds
    
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    pulse_start_time = time.time()
    pulse_end_time = time.time()
    
    # Wait for the ECHO pin to go HIGH (Start of pulse)
    # Added timeout to prevent infinite loop if sensor freezes
    timeout = time.time() + 0.1
    while GPIO.input(ECHO_PIN) == 0 and time.time() < timeout:
        pulse_start_time = time.time()
        
    # Wait for the ECHO pin to go LOW (End of pulse)
    timeout = time.time() + 0.1
    while GPIO.input(ECHO_PIN) == 1 and time.time() < timeout:
        pulse_end_time = time.time()
        
    # Calculate duration
    duration = pulse_end_time - pulse_start_time
    
    # Speed of sound is 34300 cm/s
    distance_cm = (duration * 34300) / 2
    
    # Prints the distance in the terminal & Cloud
    print(f"Distance (cm): {distance_cm:.2f}")
    
    # Send distance to V6 (rounded to 2 decimal places)
    Spell_iot.write("V6", round(distance_cm, 2))

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
