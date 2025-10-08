import gtts

# Make the text you want to convert in to speech
text = 'Hello, My name is Jarvis, and this is my voice'

# Create a variable to change the text in to speech
text_to_speech = gtts.gTTS(text)

# Save the audio data using save funtion. variable_name.save(audio_name.mp3)
text_to_speech.save('basic.mp3')
