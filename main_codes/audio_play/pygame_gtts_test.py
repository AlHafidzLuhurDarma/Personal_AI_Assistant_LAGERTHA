import gtts
import pygame

text = 'See you soon, Space Cowboy!'
speech = gtts.gTTS(text)
name_file = 'spaceCowboy.mp3'
speech.save(name_file)

pygame.mixer.init()
pygame.mixer.music.load(name_file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)