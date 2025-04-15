# LLM as a judge
# or
# intersection vs differences, e.g. show intersection in bold, while questioning/analyzing differences (list of sources, for both)
import json

# Define the file path (same as before)
file_path = r"C:\CAS NLP\FinalProject\Data\sample_data.json"

try:
    # Open the file in read mode ('r')
    with open(file_path, 'r') as f:
        # Load the JSON data from the file
        loaded_data = json.load(f)

    # Print the loaded data to the console
    print("Content of the JSON file:")
    print(json.dumps(loaded_data, indent=4))  # Use json.dumps for pretty printing

except FileNotFoundError:
    print(f"Error: File not found at '{file_path}'")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{file_path}'. The file might be corrupted.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")