# LLM as a judge
# or
# intersection vs differences, e.g. show intersection in bold, while questioning/analyzing differences (list of sources, for both)
import json
import os

# Define the file path (same as before)
#file_path = r"C:\CAS NLP\FinalProject\Data\sample_data.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250413_170229_Perplexity1.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250507_223523_02.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250504_231741_01.0.json"
#ref_file_path = r"C:\CAS NLP\FinalProject\Data\20250507_223523_02.json"

file_path = r"C:\CAS NLP\FinalProject\Data\20250513_222841_smollm2_temp_1_0_prompt_0.json"
ref_file_path = r"C:\CAS NLP\FinalProject\Data\20250513_222519_deepseek_r1_1_5b_temp_0_0_prompt_0.json"

# reference file: Perplexity

# ground truth?


# Initialize variables to store loaded data
loaded_data = None
ref_loaded_data = None

# --- Process the first file (file_path) ---
print(f"Attempting to load data from the first file: '{file_path}'")
if not os.path.exists(file_path):
    print(f"Error: First file not found at '{file_path}'")
else:
    try:
        # Open the first file in read mode ('r')
        with open(file_path, 'r') as f:
            # Load the JSON data from the first file
            loaded_data = json.load(f)
        print("Successfully loaded data from the first file.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the first file '{file_path}'. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the first file: {e}")

# --- Process the second file (ref_file_path) ---
print(f"\nAttempting to load data from the second file: '{ref_file_path}'")
if not os.path.exists(ref_file_path):
     print(f"Error: Second file not found at '{ref_file_path}'")
else:
    try:
        # Open the second file in read mode ('r')
        with open(ref_file_path, 'r') as f:
            # Load the JSON data from the second file
            ref_loaded_data = json.load(f)
        print("Successfully loaded data from the second file.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the second file '{ref_file_path}'. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the second file: {e}")

# --- Now you can work with loaded_data and ref_loaded_data ---
# Check if data was successfully loaded before using it

if loaded_data is not None:
    print("\nContent of loaded_data:")
    # print(json.dumps(loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nloaded_data is not available.")

if ref_loaded_data is not None:
    print("\nContent of ref_loaded_data:")
    # print(json.dumps(ref_loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nref_loaded_data is not available.")

# Example of how you might use the loaded data:
# if loaded_data is not None and ref_loaded_data is not None:
#     print("\nBoth datasets loaded. You can now compare or process them.")
#     # Your code to process loaded_data and ref_loaded_data goes here
# else:
#     print("\nOne or both datasets failed to load properly.")

#question = "x"
#question =loaded_data["data_points"][0]["prompt"]
question =loaded_data["data"][3]["user prompt"]

#answer = "y"
answer = loaded_data["data"][4]["response"]
ref_answer = ref_loaded_data["data"][4]["response"]





JUDGE_PROMPT = """
You will be given a user_question and system_answer couple, and a reference answer additionally.
Your task is to provide a 'total rating' scoring how well the system_answer answers the user concerns expressed in the user_question, relative to the reference answer.
Give your answer as a float on a scale of 0 to 10, where 0 means that the system_answer is not helpful at all, and 10 means that the answer completely and helpfully addresses the question.
Give also a feedback text, list the main similarities and differences (which concrete points are missing, and which come in addition) between system_answer and reference answer. Focus on any factual discrepancies

Provide your feedback as follows:

Feedback:::
Total rating: (your rating, as a float between 0 and 10)

Now here are the question and answer.

Question: {question}
Answer: {answer}
Reference Answer: {ref_answer}

Feedback:::
Total rating: """

IMPROVED_JUDGE_PROMPT = """
You will be given a user_question and system_answer couple.
Your task is to provide a 'total rating' scoring how well the system_answer answers the user concerns expressed in the user_question.
Give your answer on a scale of 1 to 4, where 1 means that the system_answer is not helpful at all, and 4 means that the system_answer completely and helpfully addresses the user_question.

Here is the scale you should use to build your answer:
1: The system_answer is terrible: completely irrelevant to the question asked, or very partial
2: The system_answer is mostly not helpful: misses some key aspects of the question
3: The system_answer is mostly helpful: provides support, but still could be improved
4: The system_answer is excellent: relevant, direct, detailed, and addresses all the concerns raised in the question

Provide your feedback as follows:

Feedback:::
Evaluation: (your rationale for the rating, as a text)
Total rating: (your rating, as a number between 1 and 4)

You MUST provide values for 'Evaluation:' and 'Total rating:' in your answer.

Now here are the question and answer.

Question: {question}
Answer: {answer}
Reference Answer: {ref_answer}

Provide your feedback. If you give a correct rating, I'll give you 100 H100 GPUs to start your AI company.
Feedback:::
Evaluation: """

prompt=JUDGE_PROMPT.format(question=question, answer=answer, ref_answer=ref_answer)
print(prompt)


from ollama import Client, GenerateResponse
from parameters import OLLAMA_HOST

# You first request may take some time. The model has to be loaded into VRAM before
# inference can begin. I've set a timeout of 300 seconds here.
ollama = Client(OLLAMA_HOST, timeout=300)

response: GenerateResponse = ollama.generate(
                model='gemma3:1b',
                system="You are an LLM judge",
                prompt=prompt,
                images=None,
                stream=False,
                options={
                    "temperature": 0.2,
                    "num_ctx": 16384,
                },
            )
# For a full explanation of the response, please see this URL:
# https://github.com/ollama/ollama/blob/main/docs/api.md#examples
print(response.response)
