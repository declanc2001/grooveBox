import RPi.GPIO as GPIO
import time

LED_PIN = 17
BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            GPIO.output(LED_PIN, True)
        else:
            GPIO.output(LED_PIN, False)

        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
