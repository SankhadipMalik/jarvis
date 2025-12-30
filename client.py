from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)