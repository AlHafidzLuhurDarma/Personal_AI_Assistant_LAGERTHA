import openai

openai.api_key = "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"

messages = []
messages.append({"role" : "system", "content" : "An AI named Lagertha"})

print("Lagertha is ready!!")

while True:
    message = input("")
    messages.append({"role" : "user", "content" : message})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role" : "assistant", "content": reply})
    print("\n" + reply + "\n")