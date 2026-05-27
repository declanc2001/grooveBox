import RPi.GPIO as GPIO
import time

LED_ACTIVE = 17
LED_STEP = 18
BUTTON_TOGGLE = 27
BUTTON_PLAY = 22

GATE_FILE = "/home/declanc01/grooveBox/gate.txt"
FREQ_FILE = "/home/declanc01/grooveBox/freq.txt"
SELECTED_FREQ_FILE = "/home/declanc01/grooveBox/selected_freq.txt"
BPM_FILE = "/home/declanc01/grooveBox/bpm.txt"


GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_ACTIVE, GPIO.OUT)
GPIO.setup(LED_STEP, GPIO.OUT)
GPIO.setup(BUTTON_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

steps = 16
time.sleep(0.08)
GPIO.output(LED_STEP, 0)



# None = step off, number = stored frequency
sequence = [None] * steps

playing = True

def read_bpm():
    try:
        with open(BPM_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 120
    
def write_gate(value):
    with open(GATE_FILE, "w") as f:
        f.write(str(value))

def write_freq(freq):
    with open(FREQ_FILE, "w") as f:
        f.write(str(freq))

def read_selected_freq():
    try:
        with open(SELECTED_FREQ_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 220

print("Sequencer ready")
print("Turn potentiometer to choose note")
print("Press toggle to save/remove note on current step")

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

            selected_freq = read_selected_freq()

            print("STEP:", i, "VALUE:", sequence[i], "SELECTED:", selected_freq)

            GPIO.output(LED_STEP, 1)

            # Toggle current step
            if GPIO.input(BUTTON_TOGGLE) == 1:

              press_start = time.time()

              while GPIO.input(BUTTON_TOGGLE) == 1:
                time.sleep(0.01)

              press_length = time.time() - press_start

              selected_freq = read_selected_freq()

              if sequence[i] is None:

                if press_length > 0.5:
                  sequence[i] = {"freq": selected_freq, "slide": 1}
                  print("SAVED SLIDE STEP", i, "AS", selected_freq, "Hz")
                else:
                  sequence[i] = {"freq": selected_freq, "slide": 0}
                  print("SAVED STEP", i, "AS", selected_freq, "Hz")

              else:
                  sequence[i] = None
                  print("CLEARED STEP", i)

              time.sleep(0.25)

            # Play stored note if step is active
            if sequence[i] is not None:
               GPIO.output(LED_ACTIVE, 1)
               write_freq(sequence[i]["freq"])

               with open("/home/declanc01/grooveBox/slide.txt", "w") as f:
                  f.write(str(sequence[i]["slide"]))

               write_gate(1)

            else:
               GPIO.output(LED_ACTIVE, 0)

               with open("/home/declanc01/grooveBox/slide.txt", "w") as f:
                  f.write("0")

               write_gate(0)

            time.sleep(0.08)

            GPIO.output(LED_STEP, 0)

            tempo = read_bpm()
            step_time = 60 / tempo / 4

            remaining = step_time - 0.08
            if remaining > 0:
             time.sleep(remaining)

            remaining = step_time - 0.08
            if remaining > 0:
                time.sleep(remaining)

except KeyboardInterrupt:
    pass

finally:
    write_gate(0)
    GPIO.output(LED_STEP, 0)
    GPIO.output(LED_ACTIVE, 0)
    GPIO.cleanup()