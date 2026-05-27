import spidev
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# OLED setup
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# C minor / acid-style bass notes
notes = [
    ("C1", 33),
    ("D#1", 39),
    ("F1", 44),
    ("G1", 49),
    ("A#1", 58),

    ("C2", 65),
    ("D#2", 78),
    ("F2", 87),
    ("G2", 98),
    ("A#2", 117),

    ("C3", 131),
    ("D#3", 156),
    ("F3", 175),
    ("G3", 196),
    ("A#3", 233),

    ("C4", 262),
]

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

try:
    while True:
        pot = read_channel(0)
        cutoff_pot = read_channel(1)
        tempo_pot = read_channel(2)
        decay_pot = read_channel(3)

        bpm = int(60 + (tempo_pot / 1023) * 120)
        cutoff = 300 + int((cutoff_pot / 1023) * 700)
        decay = 9990 + int((decay_pot / 1023) * 9)

        with open("/home/declanc01/grooveBox/cutoff.txt", "w") as f:
          f.write(str(cutoff))


        index = int((pot / 1023) * (len(notes) - 1))
        note_name, freq = notes[index]

        with open("/home/declanc01/grooveBox/selected_freq.txt", "w") as f:
          f.write(str(freq))

        with open("/home/declanc01/grooveBox/bpm.txt", "w") as f:
          f.write(str(bpm))  

        with open("/home/declanc01/grooveBox/decay.txt", "w") as f:
          f.write(str(decay))


          

        with canvas(device) as draw:
         draw.text((5, 15), f"BPM:{bpm}", fill="white")
         draw.text((5, 25), f"NOTE: {note_name}", fill="white")
         draw.text((5, 45), f"Cut off (hz):{cutoff}", fill="white")

        time.sleep(0.05)

except KeyboardInterrupt:
    spi.close()