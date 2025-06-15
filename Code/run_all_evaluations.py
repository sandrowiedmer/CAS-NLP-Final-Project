import os
import re
from evaluation import run_evaluation  # Import the evaluation function

# --- Configuration ---
#directory_path_response = r"C:\CAS NLP\FinalProject\Data\Responses"  # Your responses directory
directory_path_response = r"C:\CAS NLP\FinalProject\Data\Benchmark"  # Your responses directory

directory_path_reference = r"C:\CAS NLP\FinalProject\Data\Benchmark"  # Directory where reference models are located (can be the same as responses)

# The name of your single fixed reference model (as it appears in filenames, e.g., 'perplexityresearch')
REFERENCE_MODEL_NAME = "chatgptdeepresearch"

# List of user prompt indices to evaluate (0 to 7)
#USER_PROMPT_INDICES_TO_EVALUATE = [0, 1, 2, 3, 4, 5, 6, 7]  # Evaluate all 8 prompts

USER_PROMPT_INDICES_TO_EVALUATE = [0] # Example: Evaluate only userprompt_0 and userprompt_3

# --- End Configuration ---

def extract_file_info(filename):
    """
    Extracts timestamp, model name, temperature, and user prompt index from the filename.
    Expected format: YYYYMMDD_HHMMSS_modelname_temp_X_systprompt_Y_userprompt_Z.json
    """
    match = re.match(
        r'^(\d{8}_\d{6})_([a-zA-Z0-9_]+)_temp_(\d+[_.]?\d*)_systprompt_\d+_userprompt_(\d+)\.json$',
        filename
    )
    if match:
        timestamp_str = match.group(1)
        model_name = match.group(2)  # e.g., 'deepseek_r1_1_5b'
        temperature_str = match.group(3)  # e.g., '1_0' or '0_2'
        user_prompt_index = int(match.group(4))

        # Convert temperature string back to float for consistent processing
        try:
            temperature = float(temperature_str.replace('_', '.'))
        except ValueError:
            temperature = None  # Handle cases where temperature can't be parsed

        return timestamp_str, model_name, temperature, user_prompt_index, filename
    else:
        # print(f"Warning: Filename format mismatch for {filename}")
        return None, None, None, None, None


def find_reference_file(ref_dir, ref_model_name, user_prompt_index):
    """
    Finds the reference file for a given user prompt index and reference model.
    """
    for filename in os.listdir(ref_dir):
        # We need to parse the reference filename in the same way to ensure we get its model name
        _timestamp, model_name_from_ref_file, _temp, _user_prompt_idx_from_ref, _full_filename = extract_file_info(
            filename)

        # Ensure it's a JSON file, the user prompt index matches, and the model name matches the reference
        if filename.endswith(".json") and \
                _user_prompt_idx_from_ref == user_prompt_index and \
                model_name_from_ref_file == ref_model_name:
            return os.path.join(ref_dir, filename)
    return None


def main():
    print(f"Starting evaluation process...")
    print(f"Response directory: {directory_path_response}")
    print(f"Reference directory: {directory_path_reference}")
    print(f"Reference model: {REFERENCE_MODEL_NAME}")
    print(f"User prompts to evaluate: {USER_PROMPT_INDICES_TO_EVALUATE}")

    # Store found evaluation files, now including temperature
    evaluated_files = []
    for filename in os.listdir(directory_path_response):
        if filename.endswith(".json"):
            timestamp, model_name, temperature, user_prompt_index, full_filename = extract_file_info(filename)
            if all([timestamp, model_name, temperature is not None, user_prompt_index is not None, full_filename]):
                # Store temperature along with other info
                evaluated_files.append(
                    (model_name, temperature, user_prompt_index, os.path.join(directory_path_response, full_filename)))

    if not evaluated_files:
        print(
            "No valid response files found in the specified directory. Please check the path and file naming convention.")
        return

    # Filter evaluated_files based on desired user prompt indices
    # We now group by model and temperature combination for evaluation
    filtered_evaluated_files = [
        (model, temp, up_idx, path) for model, temp, up_idx, path in evaluated_files
        if up_idx in USER_PROMPT_INDICES_TO_EVALUATE
    ]

    if not filtered_evaluated_files:
        print("No response files found for the specified user prompt indices. Exiting.")
        return

    # Group files by (model, temperature) tuple and then by user prompt
    model_temp_prompt_files = {}
    for model, temp, up_idx, path in filtered_evaluated_files:
        model_temp_key = (model, temp)  # Use a tuple to represent model and its temperature
        if model_temp_key not in model_temp_prompt_files:
            model_temp_prompt_files[model_temp_key] = {}
        model_temp_prompt_files[model_temp_key][up_idx] = path

    # Sort models for consistent output
    sorted_model_temp_keys = sorted(model_temp_prompt_files.keys(),
                                    key=lambda x: (x[0], x[1]))  # Sort by model name then temp

    for model_temp_key in sorted_model_temp_keys:
        model_name, model_temperature = model_temp_key
        prompt_files_map = model_temp_prompt_files[model_temp_key]

        print(f"\n--- Processing Model: {model_name} (Temperature: {model_temperature}) ---")
        for user_prompt_index in USER_PROMPT_INDICES_TO_EVALUATE:
            eval_file_path = prompt_files_map.get(user_prompt_index)
            if eval_file_path:
                ref_file_path = find_reference_file(directory_path_reference, REFERENCE_MODEL_NAME, user_prompt_index)

                if ref_file_path:
                    # run_evaluation now takes the specific evaluated model's name and temperature
                    # to pass to save_judgment.
                    # Note: run_evaluation must be adapted to accept these parameters if it doesn't already.
                    # We'll assume run_evaluation passes these on to save_judgment.
                    print(
                        f"--- Evaluating: {os.path.basename(eval_file_path)} against {os.path.basename(ref_file_path)} ---")
                    run_evaluation(eval_file_path,
                                   ref_file_path)  # Pass just the paths, save_judgment reads info internally
                else:
                    print(
                        f"Warning: Reference file for userprompt_{user_prompt_index} not found for model '{REFERENCE_MODEL_NAME}' in '{directory_path_reference}'. Skipping evaluation for {os.path.basename(eval_file_path)}")
            else:
                print(
                    f"Warning: Response file for model '{model_name}' (Temp: {model_temperature}) and userprompt_{user_prompt_index} not found. Skipping.")

    print("\nEvaluation process completed.")


if __name__ == "__main__":
    main()