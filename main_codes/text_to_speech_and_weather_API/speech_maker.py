import gtts
import pygame

text = "LED Gradient has been confirm!"
speech = gtts.gTTS(text)
name_file = ("LED_Confirmation.mp3")
speech.save(name_file)

pygame.mixer.init()
pygame.mixer.music.load(name_file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)