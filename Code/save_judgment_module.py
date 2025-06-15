import json
import os
import re
import datetime

def _sanitize_model_name(model_name_original):
    """
    Sanitizes an original model name to be filesystem-safe (alphanumeric with underscores).
    e.g., "deepseek-r1:1.5b" -> "deepseek_r1_1_5b"
    """
    # Replace non-alphanumeric characters (except underscore) with underscore
    # Then ensure no multiple underscores and leading/trailing underscores are removed
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', model_name_original).lower()
    safe_name = re.sub(r'_{2,}', '_', safe_name) # Replace multiple underscores with single
    safe_name = safe_name.strip('_') # Remove leading/trailing underscores
    return safe_name

def _sanitize_temp_for_filename(temperature_float):
    """
    Converts a float temperature to a filename-safe string (e.g., 0.2 -> "0_2").
    """
    return str(temperature_float).replace('.', '_')


def save_judgment(evalfilename, reffilename, judge_model_original, judge_temperature_original, judgment_response_text, prompt_eval_count, eval_count):
    """
    Saves the evaluation judgment to a JSON file.
    Stores original model names and temperatures in JSON.
    Uses sanitized names/temps for the JSON filename.
    """
    judgments_dir = r"C:\CAS NLP\FinalProject\Data\Judgments"
    os.makedirs(judgments_dir, exist_ok=True)

    # --- Extract evaluated model info from evalfilename ---
    # We still need to parse the *evaluated model's original name and temperature*
    # from its filename because the evalfilename comes from save_response,
    # which uses the sanitized names in its filename.
    evaluated_model_name_in_filename = "unknown_model_filename" # The sanitized name from evalfilename
    user_prompt_index = "unknown"
    eval_timestamp_str = "unknown_timestamp"
    evaluated_model_temp_in_filename = None # The temp from evalfilename, as string with underscores

    eval_basename = os.path.basename(evalfilename)

    # Regex to extract timestamp, SANITIZED model name, SANITIZED evaluated temp, and userprompt
    # This regex is adjusted to correctly capture the model name as it appears *in the filename*
    # which should already be sanitized by your `save_response` function.
    match = re.search(r'^(\d{8}_\d{6})_([a-zA-Z0-9_]+)_temp_(\d+[_.]?\d*)(?:_\d+)?_systprompt_\d+_userprompt_(\d+)\.json$', eval_basename)

    if match:
        eval_timestamp_str = match.group(1)
        evaluated_model_name_in_filename = match.group(2) # This is the sanitized name from evalfilename
        try:
            temp_str = match.group(3).replace('_', '.') # Convert back to float friendly string
            evaluated_model_temp_in_filename = float(temp_str) # This is the original float temperature
        except ValueError:
            evaluated_model_temp_in_filename = None
        user_prompt_index = int(match.group(4))
    else:
        print(f"Warning: Could not parse evaluated model info from filename: {eval_basename}. Using defaults.")


    # --- Parse the Total Rating from the judgment_response_text ---
    total_rating = None
    rating_match = re.search(r'1\.\)\s*Total rating:\s*(\d+)', judgment_response_text)
    if rating_match:
        try:
            total_rating = int(rating_match.group(1))
            if not (1 <= total_rating <= 4):
                print(f"Warning: Extracted total rating {total_rating} is outside expected range (1-4) in {eval_basename}")
        except ValueError:
            print(f"Warning: Could not convert extracted rating to integer in {eval_basename}")
    else:
        print(f"Warning: Could not find 'Total rating:' in judgment response for {eval_basename}")

    # --- Prepare data for JSON ---
    # Store original model and temperature values directly in the JSON
    judgment_data = {
        "eval_file_path": evalfilename,
        "ref_file_path": reffilename,
        "judge_model": judge_model_original, # Store judge model name
        "judge_temperature": judge_temperature_original, # Store judge temperature
        "evaluated_model_name": evaluated_model_name_in_filename, # Store the sanitized name for consistency with filename parsing
        "user_prompt_index": user_prompt_index,
        "evaluated_model_temp": evaluated_model_temp_in_filename, # Store evaluated model temperature
        "total_rating": total_rating,
        "judgment_response_text": judgment_response_text,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": eval_count
    }

    # --- Construct Output Filename (using sanitized versions) ---
    # These are used for the actual judgment JSON file name
    sanitized_evaluated_model_name = _sanitize_model_name(evaluated_model_name_in_filename) # Ensure it's sanitized again just in case
    sanitized_judge_model_name = _sanitize_model_name(judge_model_original)
    sanitized_judge_temperature_filename = _sanitize_temp_for_filename(judge_temperature_original)

    current_time = datetime.datetime.now()
    judgment_timestamp_str = current_time.strftime("%Y%m%d_%H%M%S") # New timestamp for the judgment file itself

    output_filename = os.path.join(judgments_dir,
                                   f"judgment_{sanitized_evaluated_model_name}"
                                   f"_userprompt_{user_prompt_index}"
                                   f"_judge_{sanitized_judge_model_name}"
                                   f"_temp_{sanitized_judge_temperature_filename}"
                                   f"_{judgment_timestamp_str}.json")

    try:
        with open(output_filename, 'w') as f:
            json.dump(judgment_data, f, indent=4)
        print(f"Judgment saved to: '{output_filename}'")
    except Exception as e:
        print(f"Error saving judgment to JSON file: {e}")