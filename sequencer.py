import RPi.GPIO as GPIO
import time

LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

steps = 16
tempo = 120

step_time = 60/tempo/4

while True:

    for i in range(steps):

        print("STEP:", i)

        GPIO.output(LED_PIN, 1)
        time.sleep(0.05)

        GPIO.output(LED_PIN, 0)
        time.sleep(step_time)