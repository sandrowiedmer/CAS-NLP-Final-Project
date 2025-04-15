#!pip install ollama
#!pip install httpx
import ollama

#OLLAMA_HOST = "https://ollama-ha.comet-lab.group"
OLLAMA_HOST =  "http://localhost:11434"

SYSTEM_PROMPT = """\
You are a writer for a publishing company in the United States who writes original stories about classic characters.\
"""

USER_PROMPT = """\
Write a sequel to the story of Peter Pan.\
"""

from pprint import pprint

import httpx

response = httpx.get(OLLAMA_HOST + "/api/tags")

pprint(response.json())

response = httpx.get(OLLAMA_HOST + "/api/ps")

pprint(response.json())

from ollama import Client, GenerateResponse

# You first request may take some time. The model has to be loaded into VRAM before
# inference can begin. I've set a timeout of 300 seconds here.
ollama = Client(OLLAMA_HOST, timeout=300)

# Simple generate, non-streaming


response: GenerateResponse = ollama.generate(
    #model="llama3.1:8b",  # SmartLab
    #model="deepseek-r1:32b", # SmartLab
    model = 'gemma3:1b',
    system=SYSTEM_PROMPT,
    prompt=USER_PROMPT,
    images=None,
    stream=False,
    #format=JSON,

    # Please see here for options:
    # https://github.com/ollama/ollama/blob/main/docs/modelfile.md#parameter
    options={
        # Higher is more "creative", but more prone to hallucinations
        "temperature": 0.8,  # Float between 0.0 and 1.0
        # The default value for Ollama is 2048, which is quite small.
        # Please do not exceed 4096 for the bigger models and 16384 for the smaller models
        # Increasing the `num_ctx` will increase the VRAM usage. Given a high enough number,
        # there may not enough VRAM for everyone else to use.
        "num_ctx": 16384,
    },
)

# For a full explanation of the response, please see this URL:
# https://github.com/ollama/ollama/blob/main/docs/api.md#examples
print(response.response)
print(response.json)
