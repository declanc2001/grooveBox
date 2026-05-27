import pygame
import time

pygame.mixer.init()

sound = pygame.mixer.Sound("/home/declanc01/grooveBox/samples/initialsample.wav")
sound.set_volume(1.0)

print("playing...")
sound.play()

time.sleep(2)