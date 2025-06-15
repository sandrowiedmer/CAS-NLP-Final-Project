import json
import os
from ollama import Client, GenerateResponse
from parameters import OLLAMA_HOST, judge_model, judge_temperature
from save_judgment_module import save_judgment

# Reference Guided Judge Prompt
JUDGE_PROMPT = """
Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below, with a reference answer to be used as a benchmark. Your evaluation should consider factual correctness, relevance, accuracy and helpfulness, again guided by the reference. You will be given a reference answer and the assistant’s answer. Begin your evaluation by comparing the assistant's answer with the reference answer.
Identify and correct any mistakes in the assistant's answer, according to the reference answer. Avoid any position biases and ensure that the order in which the responses were presented does not influence your decision. Do not allow the length of the responses to influence your evaluation. Do not favor certain names of the assistants. Be as objective as possible.

Your task is to provide a 'total rating' scoring how well the assistant’s answer answers the user concerns expressed in the user question, guided by the given reference answer.
Give your answer on a scale of 1 to 4, where 1 means that the assistant's answer is not helpful at all, and 4 means that the assistant's answer completely and helpfully addresses the user's question, all guided by the reference answer.

Here is the scale you should use to build your answer:
1: The assistant's answer is terrible: completely irrelevant to the question asked, or very partial
2: The assistant's answer is mostly not helpful: misses some key aspects of the question
3: The assistant's answer is mostly helpful: provides support, but still could be improved
4: The assistant's answer is excellent: relevant, direct, detailed, and addresses all the concerns raised in the question and answered in the reference answer

After providing your explanation, output your final verdict by strictly following this format:

Feedback:::
1.) Total rating: (your rating, as a number between 1 and 4)
2.) Evaluation: (your rationale for the rating, as a text)

You MUST provide values for '1.) Total rating:'  and '2.) Evaluation:' in your answer.

Now here are the question, reference answer and the assistant’s answer.

[User Question]
{question}

[The Start of Reference Answer]
{ref_answer}
[The End of Reference Answer]

[The Start of the Assistant's Answer]
{answer}
[The End of the Assistant's Answer]

Provide your feedback. If you give a correct rating, you'll get whatever you want.
Feedback:::
1.) Total rating
2.) Evaluation:
"""

def run_evaluation(eval_file_path: str, ref_file_path: str):
    """
    Runs the evaluation for a single pair of evaluated and reference response files.

    Args:
        eval_file_path (str): The path to the JSON file containing the evaluated model's response.
        ref_file_path (str): The path to the JSON file containing the reference model's response.
    """

    print(f"\n--- Evaluating: {os.path.basename(eval_file_path)} against {os.path.basename(ref_file_path)} ---")

    loaded_data = None
    ref_loaded_data = None

    # Load evaluated data
    if not os.path.exists(eval_file_path):
        print(f"Error: Evaluated file not found at '{eval_file_path}'")
        return
    try:
        with open(eval_file_path, 'r') as f:
            loaded_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{eval_file_path}'. File might be corrupted.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while processing '{eval_file_path}': {e}")
        return

    # Load reference data
    if not os.path.exists(ref_file_path):
        print(f"Error: Reference file not found at '{ref_file_path}'")
        return
    try:
        with open(ref_file_path, 'r') as f:
            ref_loaded_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{ref_file_path}'. File might be corrupted.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while processing '{ref_file_path}': {e}")
        return

    if loaded_data is None or ref_loaded_data is None:
        print("Skipping evaluation due to loading errors.")
        return

    try:
        # Extract question and answers based on your specified JSON structure
        #question = loaded_data["data"]["user_prompt"] # dictionary
        #answer = loaded_data["data"]["response"] # dictionary
        question = loaded_data["data"][3]["user prompt"]  #
        answer = loaded_data["data"][4]["response"]  #
        ref_answer = ref_loaded_data["data"][4]["response"] # list of dictionaries, as saved with previous save routine
    except KeyError as e:
        print(f"Error: Missing expected key in JSON data: {e}. Check file structure.")
        return
    except IndexError as e:
        print(f"Error: Index out of range when accessing 'data' list: {e}. Check file structure.")
        return


    prompt = JUDGE_PROMPT.format(question=question, answer=answer, ref_answer=ref_answer)
    # print("\n--- JUDGE PROMPT ---")
    # print(prompt) # Uncomment to debug the prompt if needed
    # print("--------------------")

    try:
        ollama = Client(OLLAMA_HOST, timeout=300)
        response: GenerateResponse = ollama.generate(
                        model=judge_model,
                        system="You are an LLM judge. ",
                        prompt=prompt,
                        images=None,
                        stream=False,
                        options={
                            "temperature": judge_temperature,
                            "num_ctx": 16384,
                        },
                    )
        print("Ollama response received.")
        # print(response.response) # Uncomment to see raw Ollama response

        # Save judgment
        save_judgment(eval_file_path, ref_file_path, judge_model, judge_temperature, response.response, response.prompt_eval_count, response.eval_count)
        print(f"Judgment saved for {os.path.basename(eval_file_path)}.")

    except Exception as e:
        print(f"An error occurred during Ollama generation or saving judgment: {e}")