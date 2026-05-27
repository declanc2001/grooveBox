import subprocess
import os
import RPi.GPIO as GPIO
import time

LED_ACTIVE = 17
LED_STEP = 18
BUTTON_TOGGLE = 27
BUTTON_PLAY = 22

GATE_FILE = "/home/declanc01/grooveBox/gate.txt"

import subprocess
import time
import RPi.GPIO as GPIO

GATE_FILE = "/home/declanc01/grooveBox/gate.txt"
AUDIO_ENGINE = "/home/declanc01/grooveBox/oscillator_audio"

with open(GATE_FILE, "w") as f:
    f.write("0")

audio_proc = subprocess.Popen(["/home/declanc01/grooveBox/oscillator_audio"])
time.sleep(0.2)

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_ACTIVE, GPIO.OUT)
GPIO.setup(LED_STEP, GPIO.OUT)
GPIO.setup(BUTTON_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

steps = 16
tempo = 120
step_time = 60 / tempo / 4

sequence = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

playing = True

def write_gate(value):
    with open(GATE_FILE, "w") as f:
        f.write(str(value))

print("Sequencer ready")
print("Button on GPIO27 = toggle current step")
print("Button on GPIO22 = play/stop")

write_gate(0)

try:
    while True:

        while not playing:
            GPIO.output(LED_STEP, 0)
            GPIO.output(LED_ACTIVE, 0)
            write_gate(0)

            if GPIO.input(BUTTON_PLAY) == 1:
                playing = True
                print("PLAY")
                time.sleep(0.3)

            time.sleep(0.01)

        for i in range(steps):

            if GPIO.input(BUTTON_PLAY) == 1:
                playing = False
                print("STOP")
                write_gate(0)
                time.sleep(0.3)
                break

            print("STEP:", i, "VALUE:", sequence[i])

            GPIO.output(LED_STEP, 1)

            if GPIO.input(BUTTON_TOGGLE) == 1:
                sequence[i] = 1 - sequence[i]
                print("TOGGLED STEP", i, "->", sequence[i])
                time.sleep(0.25)

            if sequence[i] == 1:
               GPIO.output(LED_ACTIVE, 1)
               write_gate(1)
               time.sleep(step_time * 0.5)
               write_gate(0)
               GPIO.output(LED_ACTIVE, 0)
               time.sleep(step_time * 0.5)
            else:
               GPIO.output(LED_ACTIVE, 0)
               write_gate(0)
               time.sleep(step_time)

            # note length: hold gate for most of the step
            time.sleep(step_time * 0.7)

            # release note before next step
            write_gate(0)
            GPIO.output(LED_STEP, 0)
            GPIO.output(LED_ACTIVE, 0)

            # short gap between steps
            time.sleep(step_time * 0.3)

except KeyboardInterrupt:
    pass

finally:
    write_gate(0)
    audio_proc.terminate()
    GPIO.cleanup()
