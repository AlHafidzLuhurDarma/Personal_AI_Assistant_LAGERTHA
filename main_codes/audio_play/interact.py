from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pygame

def the_text(stream):
    data = stream.read(FRAMES_PER_BUFFER)
    if recognizer.AcceptWaveform(data):
        myText = recognizer.Result()
        myText = json.loads(myText)
        print(myText["text"])
        return myText['text']

pygame.mixer.init()
FRAMES_PER_BUFFER = 3200 # or 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
FRAME_RATE = 16000


model = Model(r"C:\Users\user\Downloads\Compressed\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, FRAME_RATE)

mic = pyaudio.PyAudio()
stream = mic.open(
    format = FORMAT,
    channels = CHANNELS,
    rate=FRAME_RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
print('Start Recording')
stream.start_stream()

while True:
    text_packages = the_text(stream)
    if text_packages == 'stop':
        break
    if text_packages == 'hello':
        pygame.mixer.music.load('basic.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)