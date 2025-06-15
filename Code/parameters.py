# used in generic prompts
MARKET = "semiconductor market"
PRODUCTS = "X-ray sources, X-ray tubes and X-ray generators"

# host = 1 or 2
host = 2

if host == 1:
    OLLAMA_HOST = "http://localhost:11434"
    models = ['deepseek-r1:1.5b', 'gemma3:1b', 'qwen3:1.7b', 'smollm2']  # smollm2 1.7b if size not specified
elif host == 2:
    OLLAMA_HOST = "https://ollama-ha.comet-lab.group"
    models = ['deepseek-r1:32b', 'gemma3:27b-it-q4_K_M', 'qwen3:30b']  # 'llama3.1:8b'
else:
    print('please check your host definition in parameters.py')


#
#temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
temperatures = [0.0, 1.0]

# Define the directory path
directory_path_response = r"C:\CAS NLP\FinalProject\Data\Responses"
directory_path_aggregation = r"C:\CAS NLP\FinalProject\Data\Aggregation"
directory_path_judgment = r"C:\CAS NLP\FinalProject\Data\Judgments"

# - Judge model definition
judge_temperature = 0.1
#judge_model = 'gemma3:1b'
#judge_model = 'smollm2'
#judge_model = 'deepseek-r1:1.5b'
judge_model = 'qwen3:1.7b'

# - Aggregation model definition
aggregate_temperature = 0.1
#judge_model = 'gemma3:1b'
#judge_model = 'smollm2'
#judge_model = 'deepseek-r1:1.5b'
aggregate_model = 'qwen3:1.7b'
