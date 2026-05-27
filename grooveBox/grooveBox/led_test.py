import RPi.GPIO as GPIO

LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, 1)

input("LED should be on now. Press Enter to quit.")

GPIO.cleanup()