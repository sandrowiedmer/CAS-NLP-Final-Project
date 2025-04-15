"""import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Tell me an interesting fact about elephants",
        },
    ],
)
print(response["message"]["content"])
"""
# Note: In the message argument, you can also add a system prompt and assistant prompt to add the context.

from ollama import chat
from ollama import ChatResponse

model1='deepseek-r1:1.5b'
model2='gemma3:1b'
model3 = 'smollm2' # 135M, 360M, or 1.7B parameters

#model4 = qwen?


#response: ChatResponse = chat(model='llama3.2', messages=[
response: ChatResponse = chat(model=model3, messages=[
  {
    'role': 'user',
    #'content': 'Why is the sky blue?',
    #'content': 'Where are you from?',
    'content': 'What do you know about the different steps of the semiconductor manufacturing process, and for which steps x-ray radiation is used?',
    #'content': 'which companies are developing, manufacturing and offering X-ray sources, used in industry (automotive, electronics, semiconductor)? which products does each of the companies offer? ?',
    #'content':'please write for each definition of truth an argument why humans, and data used for training and fine-tuning of LLMs, prepared by humans, can not always tell the truth',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

print(response.json)

