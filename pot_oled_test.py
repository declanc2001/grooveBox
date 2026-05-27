import spidev
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

while True:
    pot = read_channel(0)
    freq = int(80 + (pot / 1023) * 920)

    with open("/home/declanc01/grooveBox/freq.txt", "w") as f:
        f.write(str(freq))

    with canvas(device) as draw:
        draw.text((5, 5), "GROOVEBOX", fill="white")
        draw.text((5, 25), f"POT: {pot}", fill="white")
        draw.text((5, 45), f"FREQ: {freq}Hz", fill="white")

    time.sleep(0.05)
