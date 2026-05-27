CC=gcc
CFLAGS=-Wall -Wextra -O2
LDFLAGS=-lasound

TARGET=oscillator_audio

all: $(TARGET)

$(TARGET): main.c oscillator.s
	gcc $(CFLAGS) -o $(TARGET) main.c oscillator.s $(LDFLAGS)

clean:
	rm -f $(TARGET)