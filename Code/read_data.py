import json
import os

# Define the file path (same as before)
#file_path = r"C:\CAS NLP\FinalProject\Data\sample_data.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250413_170229_Perplexity1.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250507_223523_02.json"
#file_path = r"C:\CAS NLP\FinalProject\Data\20250504_231741_01.0.json"
#ref_file_path = r"C:\CAS NLP\FinalProject\Data\20250507_223523_02.json"

file_path = r"C:\CAS NLP\FinalProject\Data\20250513_222841_smollm2_temp_1_0_prompt_0.json"
#ref_file_path = r"C:\CAS NLP\FinalProject\Data\20250513_222519_deepseek_r1_1_5b_temp_0_0_prompt_0.json"
ref_file_path = file_path

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
    print(json.dumps(loaded_data, indent=4)) # Uncomment to print the content
else:
    print("\nloaded_data is not available.")

if ref_loaded_data is not None:
    print("\nContent of ref_loaded_data:")
    print(json.dumps(ref_loaded_data, indent=4)) # Uncomment to print the content
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

print("\nContent of answer:")
print(answer) # Uncomment to print the content


print("\nContent of ref_answer:")
print(ref_answer) # Uncomment to print the content