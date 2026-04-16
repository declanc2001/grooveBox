import RPi.GPIO as GPIO
import time

LED_PIN = 17
BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)
import RPi.GPIO as GPIO
import time

LED_ACTIVE = 17
LED_STEP = 18
BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_ACTIVE, GPIO.OUT)
GPIO.setup(LED_STEP, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

steps = 16
tempo = 120

sequence = [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]

step_time = 60/tempo/4

print("Sequencer running")

try:
    while True:

        for i in range(steps):

            print("STEP:", i, "VALUE:", sequence[i])

            # step position LED
            GPIO.output(LED_STEP, 1)

            # active step LED
            if sequence[i] == 1:
                GPIO.output(LED_ACTIVE, 1)
            else:
                GPIO.output(LED_ACTIVE, 0)

            # button toggles step
            if GPIO.input(BUTTON_PIN) == 1:
                sequence[i] = 1 - sequence[i]
                print("TOGGLED STEP", i)
                time.sleep(0.25)

            time.sleep(step_time)

            GPIO.output(LED_STEP, 0)

except KeyboardInterrupt:
    GPIO.cleanup()