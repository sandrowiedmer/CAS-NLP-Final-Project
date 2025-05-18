# WebVersion of Perplexity, ChatGPT DeepResearch, Gemini (DeepResearch), Claude, mistral, DeepSeek etc. prompted & saved manually, since no API
# open deep research


#ev. compare several LLMs (what's inside the LLM? emergent..?), grouped in 2 categories:
#ollama local (small), connect to external tools? e.g. llama 3.2 + DeepSeek 1.5b
#ollama CTO Office / SmartLab (medium), connect to external tools?
#HuggingFace?

#read from prompt_collection

# existing IXM knowledge

#multiple runs per model and prompt, as answers can vary from call to call, especially with “high” temperature

#ollama list
#model1='deepseek-r1:1.5b'
#model2='gemma3:1b'
#model3 = 'smollm2'
#models = [model1, model2, model3]

from prompt_collection import system_prompt, user_prompts
from parameters import OLLAMA_HOST, models, temperatures

print(system_prompt[0])

def print_prompts_from_list():
    for i, prompt in enumerate(user_prompts):
        print(f"--- Prompt {i+1} ---")
        print(prompt)

if __name__ == "__main__":
    print_prompts_from_list()

print(models[0])
print(models[1])
print(models[2])

# call all models with all prompts in list
# save response each time in a file, prompt and model in the name


### experimental
from ollama import Client, GenerateResponse

# You first request may take some time. The model has to be loaded into VRAM before
# inference can begin. I've set a timeout of 300 seconds here.
ollama = Client(OLLAMA_HOST, timeout=300)

for model in models:
    for prompt_id, prompt in enumerate(user_prompts):
        for temperature in temperatures:
            print(f"Generating for model '{model}', prompt {prompt_id}, temp {temperature}...")

            response: GenerateResponse = ollama.generate(
                model=model,
                system=system_prompt,
                prompt=prompt,
                images=None,
                stream=False,
                options={
                    "temperature": temperature,
                    "num_ctx": 16384,
                },
            )
# For a full explanation of the response, please see this URL:
# https://github.com/ollama/ollama/blob/main/docs/api.md#examples
            print(response.response)
            print(response.json)

            from save_response_module import save_response
            save_response(model, prompt_id, temperature, response.response)