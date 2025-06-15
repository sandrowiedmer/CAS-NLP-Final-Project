#multiple runs per model and prompt, as answers can vary from call to call, especially with “high” temperature

from llm_survey_prompt_collection import system_prompt, user_prompts
from parameters import OLLAMA_HOST, models, temperatures

print(system_prompt[0])

def print_prompts_from_list():
    for i, prompt in enumerate(user_prompts):
        print(f"--- Prompt {i+1} ---")
        print(prompt)

if __name__ == "__main__":
    print_prompts_from_list()

print(models)

# call all models with all prompts in list
# save response each time in a file, prompt and model in the name


### experimental
from ollama import Client, GenerateResponse

# You first request may take some time. The model has to be loaded into VRAM before
# inference can begin. I've set a timeout of 300 seconds here.
ollama = Client(OLLAMA_HOST, timeout=300)

syst_prompt_id: int = 0

for model in models:
    for prompt_id, prompt in enumerate(user_prompts):
        for temperature in temperatures:
            print(f"Generating for model '{model}', user prompt {prompt_id}, temp {temperature}...")

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

            print(response.response)
            print(response.json)

            from save_response_module import save_response
            save_response(model, syst_prompt_id, prompt_id, response.prompt_eval_count, temperature, response.response, response.eval_count)