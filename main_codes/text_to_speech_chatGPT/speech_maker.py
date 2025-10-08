import gtts
import pygame

text = "Closing the program. Have a great day!"
speech = gtts.gTTS(text)
name_file = ("Closing_off.mp3")
speech.save(name_file)

pygame.mixer.init()
pygame.mixer.music.load(name_file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)