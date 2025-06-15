def save_aggregation(reffilename1, reffilename2, reffilename3, aggregate_model, aggregate_temperature, aggregation_response, prompt_eval_count, eval_count):
    from llm_survey_prompt_collection import system_prompt, user_prompts
    from parameters import directory_path_aggregation, models
    import json
    import datetime
    import os
    import re


    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time for the filename
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    # Construct the filename
    #file_name = f"{timestamp_str}_{predefined_string}.json"
    file_name = f"{timestamp_str}_Aggregation.json"


    # Construct the full file path
    file_path = os.path.join(directory_path_aggregation, file_name)

    # Predefined data
    sample_data = {
        "description": f"This is data saved with a timestamp, containing 3 ref file names, aggregate model name, aggregate temperature, aggregate response content and prompt/response token count.",
        "timestamp": now.isoformat(),
        "data": [
        {

                "reference file name 1": reffilename1},
            {
                "reference file name 2": reffilename2},
            {
                "reference file name 3": reffilename3},
            {
                "aggregation model": aggregate_model},
            {
                "aggregation temperature": aggregate_temperature},
            {
                "prompt token count": prompt_eval_count},
            {
                "aggregation response (LLM-generated benchmark)": aggregation_response},
            {
                "response token count": eval_count}
        ]
    }

    # Ensure the directory exists
    os.makedirs(directory_path_aggregation, exist_ok=True)

    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as f:
            # Save the sample data to the JSON file with indentation
            json.dump(sample_data, f, indent=4)
        print(f"Sample data saved to '{file_path}'")

    except Exception as e:
        print(f"Error saving to JSON file: {e}")

    return f"File successfully saved"