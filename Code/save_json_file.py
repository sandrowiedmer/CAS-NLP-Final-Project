""" save the answers into a json file, in following format
output_data = {

"timestamp": datetime.datetime.now().isoformat(), #  timezone: UTC + 2h

"output": llm_output
"prompt": {

"user": user_prompt_user,

"content": user_prompt_content

},

"model": model_name,

"temperature": temperature

}

"""

import json
import datetime
import os

# Define the directory path
directory_path = r"C:\CAS NLP\FinalProject\Data"

# Define the predefined string for the filename
predefined_string = "my_sample_data" # model + prompt ID?

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time for the filename
timestamp_str = now.strftime("%Y%m%d_%H%M%S")

# Construct the filename
file_name = f"{timestamp_str}_{predefined_string}.json"

# Construct the full file path
file_path = os.path.join(directory_path, file_name)

# Predefined sample data
sample_data = {
    "description": "This is sample data saved with a timestamp.",
    "timestamp": now.isoformat(),
    "data_points": [
        {"value": 10},
        {"value": 25},
        {"value": 15}
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