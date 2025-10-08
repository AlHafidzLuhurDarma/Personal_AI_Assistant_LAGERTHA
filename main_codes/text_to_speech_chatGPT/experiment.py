import openai
import pygame
import gtts

openai.api_key = "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"

messages = []
messages.append({"role" : "system", "content" : "An AI named Lagertha that always have simple and fun answer to any kind of question, just like a friend"})

number_voice = 1
print("Lagertha is ready!!")
while True:
    number_voice += 1
    message = input("")
    if message == 'stop':
        break
    
    messages.append({"role" : "user", "content" : message})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role" : "assistant", "content": reply})
    print("\n" + reply + "\n")
    
    # Speech
    speech = gtts.gTTS(reply)
    name_file = (f"GPT_Voice_{number_voice}.mp3")
    speech.save(name_file)

    pygame.mixer.init()
    pygame.mixer.music.load(name_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.wait(10)