#!/bin/bash

cd /home/declanc01/grooveBox

cleanup() {
    echo "Stopping GrooveBox..."

    echo 0 > gate.txt

    pkill -f oscillator_audio
    pkill -f pot_oled_test.py
    pkill -f sequencer_two_leds.py

    python3 - <<'PY'
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for pin in [17, 18]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
GPIO.cleanup()
PY

    clear
    exit
}

trap cleanup INT TERM

echo "Starting GrooveBox..."

./oscillator_audio &
python3 pot_oled_test.py &
python3 sequencer_two_leds.py &

echo "GrooveBox running. Press Ctrl+C to stop."

wait