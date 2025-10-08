import pygame

# Activate the mixer
pygame.mixer.init()

# Load the audio
pygame.mixer.music.load('greenOff_led.mp3')

# Play the audio
pygame.mixer.music.play()

# Don't do anything until the audio is finished
while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)