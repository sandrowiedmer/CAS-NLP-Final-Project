import json
import datetime
import os
import re

def create_new_string(model, temperature, syst_prompt_id, user_prompt_id):
    """
    Generates a filename safe for file systems using model name, temperature, and prompt ID.

    Args:
        model_name (str): The name of the model (e.g., "deepseek-r1:1.5b").
        temperature (float): The temperature value (e.g., 0.2).
        syst_prompt_id (int): The ID of the system prompt (e.g., 0).
        user_prompt_id (int): The ID of the user prompt (e.g., 1).

    Returns:
        str: A safe filename part.
    """
    # 1. Transform Model Name
    safe_model_name = re.sub(r'[^a-zA-Z0-9]', '_', model).lower()
    safe_model_name = re.sub(r'_{2,}', '_', safe_model_name).strip('_') # Clean up multiple/edge underscores

    # 2. Transform Temperature (dot to underscore for filename)
    safe_temperature = str(temperature).replace('.', '_')

    # 3. System Prompt ID (already alphanumeric)
    safe_syst_prompt_id = str(syst_prompt_id)

    # 4. Prompt ID (already alphanumeric)
    safe_user_prompt_id = str(user_prompt_id)

    # 5. Construct Filename part
    new_string = f"{safe_model_name}_temp_{safe_temperature}_systprompt_{safe_syst_prompt_id}_userprompt_{safe_user_prompt_id}"
    return new_string

def save_response(model, syst_prompt_id, user_prompt_id, prompt_eval_count, temperature, response, eval_count):
    """
    Saves the model response to a JSON file.
    The 'data' field now contains a single dictionary for easier parsing.
    Imports necessary modules locally within the function.
    """
    from llm_survey_prompt_collection import system_prompt, user_prompts
    from parameters import directory_path_response # Assuming this exists and points to your responses directory

    # Generate the filename part based on model, temperature, and prompt IDs
    predefined_string = create_new_string(model, temperature, syst_prompt_id, user_prompt_id)

    # Get the current date and time
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    # Construct the full filename and path
    file_name = f"{timestamp_str}_{predefined_string}.json"
    file_path = os.path.join(directory_path_response, file_name)

    # --- 'data' as a SINGLE DICTIONARY ---
    #  all data related to the response is directly under the 'data' key as a dictionary
    sample_data = {
        "description": "This is data saved with a timestamp, containing model name, temperature, system prompt, user prompt, response content and prompt/response token count.",
        "timestamp": now.isoformat(),
        "data": { # a dictionary {} instead a list [] to
            "model": model, # Original model name
            "temperature": temperature, # Original float temperature
            "system_prompt": system_prompt, # Get the actual system prompt text
            "user_prompt": user_prompts[user_prompt_id],     # Get the actual user prompt text
            "prompt_token_count": prompt_eval_count,
            "response": response,
            "response_token_count": eval_count
        }
    }

    # Ensure the output directory exists
    os.makedirs(directory_path_response, exist_ok=True)

    try:
        with open(file_path, 'w') as f:
            json.dump(sample_data, f, indent=4)
        print(f"Model response saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving model response to JSON file: {e}")

    return f"File successfully saved"