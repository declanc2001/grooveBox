import RPi.GPIO as GPIO
import time

BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Press button")

while True:

    if GPIO.input(BUTTON_PIN) == 1:
        print("BUTTON PRESSED")

    time.sleep(0.1)
