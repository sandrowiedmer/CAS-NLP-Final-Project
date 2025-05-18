from save_response_module import save_response

def get_input(prompt, default=None, cast_func=str):
    user_input = input(f"{prompt} [{default}]: ") if default is not None else input(f"{prompt}: ")
    return cast_func(user_input) if user_input else default

def get_multiline_input(prompt="Enter multiline input (end with a single '.' on a new line):"):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)

# Prompting user inputs
model = get_input("Enter model", default="Perplexity") # Perplexity, ChatGPT, Gemini, Open Deep Research
prompt_id = get_input("Enter prompt ID", default=0, cast_func=int)
temperature = 2.0
response = get_multiline_input()

# Output for confirmation (optional)
print("\n--- Parameters ---")
print(f"Model: {model}")
print(f"Prompt ID: {prompt_id}")
print(f"Temperature: {temperature}")
print(f"Response: {response}")

save_response(model, prompt_id, temperature, response)