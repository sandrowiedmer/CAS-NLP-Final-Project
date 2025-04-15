import json
import datetime
import os

# Define the directory path
directory_path = r"C:\CAS NLP\FinalProject\Data"

model = "Perplexity"

prompt_id = "1"


# Define the predefined string for the filename
predefined_string = model + prompt_id

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
        {"prompt": "what else regarding semiconductor market could be from ineterest for a company developing and selling x-ray sources?"},
        {"response": "The semiconductor industry’s push toward smaller, more complex, and heterogeneously integrated devices ensures a growing role for X-ray inspection and metrology. Companies that innovate in speed, resolution, and AI integration will capture this expanding market."}
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