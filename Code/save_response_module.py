def save_response(model, prompt_id, temperature, response):
    from prompt_collection import system_prompt, user_prompts
    from parameters import directory_path, models
    import json
    import datetime
    import os

    #model = models[model_id]
    #model = model
    # Define the predefined string for the filename
    #predefined_string = str(model_id) + str(prompt_id) + str(temperature)

    import re

    def create_new_string(model, temperature, prompt_id):
        """
        Generates a filename safe for file systems using model name, temperature, and prompt ID.

        Args:
            model_name (str): The name of the model (e.g., "deepseek-r1:1.5b").
            temperature (float): The temperature value (e.g., 0.2).
            prompt_id (int): The ID of the prompt (e.g., 1).
            file_extension (str, optional): The file extension (e.g., "txt", "json"). Defaults to "txt".

        Returns:
            str: A safe filename.
        """
        # 1. Transform Model Name
        safe_model_name = re.sub(r'[^a-zA-Z0-9]', '_', model).lower()

        # 2. Transform Temperature
        safe_temperature = str(temperature).replace('.', '_')

        # 3. Prompt ID (already alphanumeric)
        safe_prompt_id = str(prompt_id)

        # 4. Construct Filename
        new_string = f"{safe_model_name}_temp_{safe_temperature}_prompt_{safe_prompt_id}"
        return new_string

    predefined_string = create_new_string(model, temperature, prompt_id)

    #predefined_string = "prompt_" + prompt_id + "model_"+ model + "temperature_" +str(temperature)

    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time for the filename
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    # Construct the filename
    file_name = f"{timestamp_str}_{predefined_string}.json"

    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)

    # Predefined data
    sample_data = {
        "description": f"This is data saved with a timestamp, containing model name, temperature, system prompt, user prompt and response.",
        "timestamp": now.isoformat(),
        "data": [
        {
                "model": model},
            {
                "temperature": temperature},
            {
                "system prompt": system_prompt},
            {
                "user prompt": user_prompts[prompt_id]},
            {
                "response": response}
        ]
    }

    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)

    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as f:
            # Save the sample data to the JSON file with indentation
            json.dump(sample_data, f, indent=4)
        print(f"Sample data saved to '{file_path}'")

    except Exception as e:
        print(f"Error saving to JSON file: {e}")

    return f"File successfully saved"