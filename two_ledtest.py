import RPi.GPIO as GPIO
import time

LED2 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED2, GPIO.OUT)

try:
    while True:
        GPIO.output(LED2, 1)
        time.sleep(1)
        GPIO.output(LED2, 0)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()