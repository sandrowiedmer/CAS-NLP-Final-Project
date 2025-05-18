#words used in generic prompts
from streamlit.components.v1 import iframe

MARKET = "semiconductor market"
PRODUCTS = "X-ray sources, X-ray tubes and X-ray generators"


# host = 1 or 2
host = 2

if host == 1:
    OLLAMA_HOST = "https://ollama-ha.comet-lab.group"
    models = ['llama3.1:8b', 'deepseek-r1:32b']
elif host == 2:
    OLLAMA_HOST =  "http://localhost:11434"
    models = ['deepseek-r1:1.5b', 'gemma3:1b', 'smollm2']
else:
    print('please check your host definition in parameters.py')


#
#temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
temperatures = [0.0, 1.0]


# Define the directory path
directory_path = r"C:\CAS NLP\FinalProject\Data"

# - Judge model definition
judge_temperature = 0.1
judge_model = 'gemma3:1b'