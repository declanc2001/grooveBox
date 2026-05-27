import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device CE0
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

try:
    while True:
        pot_value = read_channel(0)
        print("POT:", pot_value)
        time.sleep(0.1)

except KeyboardInterrupt:
    spi.close()
