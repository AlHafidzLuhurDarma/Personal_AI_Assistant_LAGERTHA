import openai

openai.api_key = "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"

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Write a simple essay about lizard"}])
print(completion.choices[0].message.content)