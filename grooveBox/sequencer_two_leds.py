# import Raspberry Pi GPIO control library
import RPi.GPIO as GPIO

# import time for tempo
import time


# assign GPIO pins 
LED_ACTIVE = 17      # Step LED
LED_STEP = 18        # 16th note LED
BUTTON_TOGGLE = 27  # button to toggle step on/off
BUTTON_PLAY = 22    # button to play/stop sequencer


# tell Python BCM is used for pin numbers
GPIO.setmode(GPIO.BCM)


# configure pins as inputs or outputs

# LED pins OUTPUT signals (Pi controls LEDs)
GPIO.setup(LED_ACTIVE, GPIO.OUT)
GPIO.setup(LED_STEP, GPIO.OUT)

# button pins INPUT signals (Pi reads button presses)
# PUD_DOWN keeps signal stable at 0 when button not pressed
GPIO.setup(BUTTON_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# number of steps in sequencer loop
steps = 16

# tempo in beats per minute
tempo = 120

# calculate duration of each step
# 60 seconds per minute / BPM = seconds per beat
# divide by 4 for 16th notes
step_time = 60 / tempo / 4


# create a list to store which steps are active
# 0 = step off
# 1 = step on
sequence = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]


# boolean for if playing
playing = True


# print startup messages to terminal
print("Sequencer ready")
print("Button on GPIO27 = toggle current step")
print("Button on GPIO22 = play/stop")


# try allows program to exit cleanly with Ctrl+C
try:

    # main loop runs forever
    while True:


        # if sequencer is stopped, stay here
        while not playing:

            # turn LEDs off when stopped
            GPIO.output(LED_STEP, 0)
            GPIO.output(LED_ACTIVE, 0)


            # check if play button pressed
            if GPIO.input(BUTTON_PLAY) == 1:

                # change state to playing
                playing = True

                print("PLAY")

                # delay prevents button triggering multiple times(bouncing)
                time.sleep(0.3)


            # short delay so CPU isn't overloaded
            time.sleep(0.01)



        # loop through all 16 steps
        for i in range(steps):


            # check if play/stop button pressed during playback
            if GPIO.input(BUTTON_PLAY) == 1:

                # change state to stopped
                playing = False

                print("STOP")

                # debounce delay
                time.sleep(0.3)

                # break exits the step loop early
                break



            # print current step number and value (0 or 1)
            print("STEP:", i, "VALUE:", sequence[i])



            # turn on LED that shows current step position
            GPIO.output(LED_STEP, 1)



            # check if current step is active
            if sequence[i] == 1:

                # turn ON active-step LED
                GPIO.output(LED_ACTIVE, 1)

            else:

                # turn OFF active-step LED
                GPIO.output(LED_ACTIVE, 0)



            # check if toggle button is pressed
            if GPIO.input(BUTTON_TOGGLE) == 1:


                # toggle the step value
                # if 0 becomes 1
                # if 1 becomes 0
                sequence[i] = 1 - sequence[i]


                # print feedback showing change
                print("TOGGLED STEP", i, "->", sequence[i])


                
                time.sleep(0.25)



            # short delay so LED_STEP flash is visible
            time.sleep(0.08)


            # turn off step-position LED
            GPIO.output(LED_STEP, 0)



            # calculate remaining time in step
            remaining = step_time - 0.08


            # wait remaining time so tempo stays correct
            if remaining > 0:
                time.sleep(remaining)



# triggered when Ctrl+C pressed in terminal
except KeyboardInterrupt:

    # reset GPIO pins safely
    GPIO.cleanup()