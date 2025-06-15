# LLM-as-a-Judge as multi-reference-aggregator
import json
import os

file_path1 = r"C:\CAS NLP\FinalProject\Data\20250529_220940_geminideepresearch_temp_0_systprompt_0_userprompt_0.json"
file_path2 = r"C:\CAS NLP\FinalProject\Data\20250606_223903_perplexityresearch_temp_0_systprompt_0_userprompt_0.json"
file_path3 = r"C:\CAS NLP\FinalProject\Data\20250606_224433_chatgptdeepresearch_temp_0_systprompt_0_userprompt_0.json"


# Initialize variables to store loaded data
loaded_data1 = None
loaded_data2 = None
loaded_data3 = None

# --- Process the first file (file_path) ---
print(f"Attempting to load data from the first file: '{file_path1}'")
if not os.path.exists(file_path1):
    print(f"Error: First file not found at '{file_path1}'")
else:
    try:
        # Open the first file in read mode ('r')
        with open(file_path1, 'r') as f:
            # Load the JSON data from the first file
            loaded_data1 = json.load(f)
        print("Successfully loaded data from the first file.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the first file '{file_path1}'. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the first file: {e}")

# --- Process the second file  ---
print(f"\nAttempting to load data from the second file: '{file_path2}'")
if not os.path.exists(file_path2):
     print(f"Error: Second file not found at '{file_path2}'")
else:
    try:
        # Open the second file in read mode ('r')
        with open(file_path2, 'r') as f:
            # Load the JSON data from the second file
            loaded_data2 = json.load(f)
        print("Successfully loaded data from the second file.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the second file '{file_path2}'. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the second file: {e}")

# --- Now you can work with loaded_data and ref_loaded_data ---
# Check if data was successfully loaded before using it

if loaded_data1 is not None:
    print("\nContent of loaded_data:")
    #print(json.dumps(loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nloaded_data is not available.")

if file_path2 is not None:
    print("\nContent of file_path2:")
    #print(json.dumps(ref_loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nfile_path2 is not available.")



# --- Process the 3rd file  ---
print(f"\nAttempting to load data from the second file: '{file_path3}'")
if not os.path.exists(file_path3):
     print(f"Error: Second file not found at '{file_path3}'")
else:
    try:
        # Open the second file in read mode ('r')
        with open(file_path3, 'r') as f:
            # Load the JSON data from the second file
            loaded_data3 = json.load(f)
        print("Successfully loaded data from the second file.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the second file '{file_path3}'. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the second file: {e}")

# --- Now you can work with loaded_data and ref_loaded_data ---
# Check if data was successfully loaded before using it

if loaded_data1 is not None:
    print("\nContent of loaded_data:")
    #print(json.dumps(loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nloaded_data is not available.")

if file_path2 is not None:
    print("\nContent of file_path2:")
    #print(json.dumps(ref_loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nfile_path2 is not available.")

question =loaded_data1["data"][3]["user prompt"]
answer1 = loaded_data1["data"][4]["response"]
answer2 = loaded_data2["data"][4]["response"]
answer3 = loaded_data3["data"][4]["response"]


print("\n\nContent of answer1:")
print(answer1) # Uncomment to print the content

print("\n\nContent of answer2:")
print(answer2) # Uncomment to print the content

print("\n\nContent of answer3:")
print(answer3) # Uncomment to print the content

multi_reference_aggregation_prompt = """
You will be given one survey question and three reference answers.
Your task is to aggregate the three reference answers into one ground truth answer.
This ground truth will be used to evaluate responses from simple LLMs.

Provide your feedback as follows:

Feedback:::
Aggregation: (your rationale for the aggregated answer, as a text)

You MUST provide 'Aggregation:' in your answer, and nothing else.

Now here are the question and answer.

Question: {question}
Reference Answer 1: {answer1}
Reference Answer 2: {answer2}
Reference Answer 3: {answer3}

Feedback:::
Aggregation: """

prompt=multi_reference_aggregation_prompt.format(question=question, answer1=answer1, answer2=answer2, answer3=answer3)

print("\n\nThis is the aggregation prompt:")
print(prompt)


from ollama import Client, GenerateResponse
from parameters import OLLAMA_HOST, aggregate_model, aggregate_temperature

# the first request may take some time. The model has to be loaded into VRAM before
# inference can begin. I've set a timeout of 300 seconds here.
ollama = Client(OLLAMA_HOST, timeout=300)

response: GenerateResponse = ollama.generate(
                model=aggregate_model,
                system="-",
                prompt=prompt,
                images=None,
                stream=False,
                options={
                    "temperature": aggregate_temperature,
                    "num_ctx": 16384,
                },
            )
# For a full explanation of the response, please see this URL:
# https://github.com/ollama/ollama/blob/main/docs/api.md#examples
print("\n\nThis is the aggregation response:")
print(response.response)

print("\n\nThis is the number of prompt tokens:")
print(response.prompt_eval_count)

print("\n\nThis is the number of response tokens:")
print(response.eval_count)


from save_aggregation_module import save_aggregation
save_aggregation(file_path1, file_path2, file_path3, aggregate_model, aggregate_temperature, response.response, response.prompt_eval_count, response.eval_count)

