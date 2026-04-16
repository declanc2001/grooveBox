from gpiozero import LED, Button
from signal import pause

led = LED(17)
btn = Button(27)

btn.when_pressed = led.on
btn.when_released = led.off

print("Press the button. LED should light up. Ctrl+C to quit.")
pause()
