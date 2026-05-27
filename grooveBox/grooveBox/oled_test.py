from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
import time

serial = i2c(port=1, address=0x3C)

device = sh1106(serial)

while True:
    with canvas(device) as draw:
        draw.text((10, 10), "GROOVEBOX", fill="white")
        draw.text((10, 30), "TB-303 MODE", fill="white")

    time.sleep(0.1)