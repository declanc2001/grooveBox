import RPi.GPIO as GPIO

# Constants won't change. They're used here to set pin numbers:
BUTTON_PIN = 16  # The number of the pushbutton pin
LED_PIN = 18     # The number of the LED pin

# Variables will change:
button_state = 0  # Variable for reading the pushbutton status

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(LED_PIN, GPIO.OUT)           # Initialize the LED pin as an output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Initialize the pushbutton pin as a pull-up input

try:
    while True:
        # Read the state of the pushbutton value:
        button_state = GPIO.input(BUTTON_PIN)

        # Control LED according to the state of the button
        if button_state == GPIO.LOW:  # If the button is pressed
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
        else:  # Otherwise, the button is not pressed
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED

except KeyboardInterrupt:
    # Clean up GPIO on program exit
    GPIO.cleanup()
