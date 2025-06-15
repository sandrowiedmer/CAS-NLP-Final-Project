import os
import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
#JUDGMENTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Judgments\judge_qwen3_1_7b"
#JUDGMENTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Judgments\judge_qwen3_30b"
JUDGMENTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Judgments\judge_gemma3_27b"

#OUTPUT_PLOTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Evaluation_Plots\judge_qwen3_1_7b"
#OUTPUT_PLOTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Evaluation_Plots\judge_qwen3_30b"
OUTPUT_PLOTS_DIRECTORY = r"C:\CAS NLP\FinalProject\Data\Evaluation_Plots\judge_gemma3_27b"

# Expected range for total rating
EXPECTED_RATING_RANGE = (1, 4)

# --- Define the EXACT desired order for models on the X-axis ---
# Ensure these names EXACTLY match how they appear after _format_for_display function.
# If a model name in your data does not exist in this list, it will appear at the very end
# in alphabetical order.
EXPLICIT_MODEL_ORDER = [
    "chatgpt deep research",
    "gemini deep research",
    "perplexity deep research",
    "deepseek-r1:1.5b",
    "deepseek-r1:32b",
    "gemma3:1b",
    "gemma3:27b-it-q4_K_M",
    "qwen3:1.7b",
    "qwen3:30b",
    "smollm2"
]
# --- End Explicit Model Order ---


# Configure plot aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10


# --- Functions ---

def parse_judgment_file(filepath):
    """
    Reads a judgment JSON file and extracts relevant data.
    Expects 'evaluated_model_name' to be in the sanitized format (e.g., qwen3_1_7b).
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        evaluated_model_name = data.get("evaluated_model_name")  # This will be the sanitized name from JSON
        user_prompt_index = data.get("user_prompt_index")  # This is still 0-indexed from filename
        evaluated_model_temp = data.get("evaluated_model_temp")
        total_rating = data.get("total_rating")
        judge_model = data.get("judge_model")
        judge_temperature = data.get("judge_temperature")
        ref_file_path = data.get("ref_file_path")

        if total_rating is not None and not (EXPECTED_RATING_RANGE[0] <= total_rating <= EXPECTED_RATING_RANGE[1]):
            print(
                f"Warning: Rating {total_rating} for {os.path.basename(filepath)} is outside expected range {EXPECTED_RATING_RANGE}. Keeping it.")

        if any(x is None for x in
               [evaluated_model_name, user_prompt_index, evaluated_model_temp, total_rating, judge_model,
                judge_temperature, ref_file_path]):
            print(f"Warning: Missing essential data fields in {os.path.basename(filepath)}. Skipping.")
            return None

        return {
            "evaluated_model_name": evaluated_model_name,  # Stored as sanitized
            "user_prompt_index": user_prompt_index,
            "evaluated_model_temp": evaluated_model_temp,
            "total_rating": total_rating,
            "judge_model": judge_model,
            "judge_temperature": judge_temperature,
            "ref_file_path": ref_file_path
        }
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'. File might be corrupted.")
        return None
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
        return None


def _format_for_display(sanitized_name):
    """
    Attempts to reverse the sanitization of model names for display purposes.
    Handles common patterns including specific quantized models and new "deep research" names.
    """
    # New: Handle "deep research" models, assuming they are sanitized without spaces
    if sanitized_name == 'chatgptdeepresearch':
        return 'chatgpt deep research'
    if sanitized_name == 'geminideepresearch':
        return 'gemini deep research'
    if sanitized_name == 'perplexityresearch':
        return 'perplexity deep research'

    # Rule 1: Handle 'deepseek-r1' specific pattern first (e.g., deepseek_r1_1_5b -> deepseek-r1:1.5b)
    if sanitized_name.startswith('deepseek_r1_'):
        display_name = sanitized_name.replace('deepseek_r1_', 'deepseek-r1:')
        # Then convert remaining underscores in the version part to dots
        display_name = re.sub(r'(\d)_(\d+b)$', r'\1.\2', display_name)
        return display_name

    # Rule 2: Handle quantized models like 'gemma3_27b_it_q4_k_m' -> 'gemma3:27b-it-q4_K_M'
    # This pattern captures the base, the 'XXb' version, and the quantization suffix
    match_quantized = re.match(r'^(.*?)_(\d+b)(_it_q4_k_m)$', sanitized_name)
    if match_quantized:
        base_name = match_quantized.group(1)  # e.g., 'gemma3'
        version_b = match_quantized.group(2)  # e.g., '27b'
        quant_suffix = match_quantized.group(3)  # e.g., '_it_q4_k_m'

        # Transform the quantization suffix:
        # '_it_' becomes '-it-'
        # '_k_m' becomes '_K_M' (for capitalization)
        transformed_quant_suffix = quant_suffix.replace('_it_', '-it-')
        transformed_quant_suffix = transformed_quant_suffix.replace('_k_m', '_K_M')

        return f"{base_name}:{version_b}{transformed_quant_suffix}"

    # Rule 3: Handle general models like 'qwen3_1_7b' -> 'qwen3:1.7b' or 'gemma3_1b' -> 'gemma3:1b'
    # This targets names that end with _digit_digitb or _digitb
    match_version = re.match(r'^(.*?)_(\d+)(?:_(\d+))?(b)$', sanitized_name)
    if match_version:
        base = match_version.group(1)
        major_version = match_version.group(2)
        minor_version = match_version.group(3)
        unit = match_version.group(4)  # 'b'

        if minor_version:
            # e.g., 'qwen3_1_7b' -> 'qwen3:1.7b'
            return f"{base}:{major_version}.{minor_version}{unit}"
        else:
            # e.g., 'gemma3_1b' -> 'gemma3:1b'
            return f"{base}:{major_version}{unit}"

    # Default: if no specific pattern matches (e.g., 'smollm2', 'perplexity')
    return sanitized_name


def get_ref_model_name(ref_file_path):
    """
    Extracts the reference model name from its file path.
    Assumes the reference file name uses sanitized names (e.g., chatgptdeepresearch).
    """
    if ref_file_path:
        match = re.search(r'^\d{8}_\d{6}_([a-zA-Z0-9_]+)_temp_', os.path.basename(ref_file_path))
        if match:
            return match.group(1)
    return "unknown_reference"


def get_model_sort_key_from_explicit_order(model_name_for_sorting):
    """
    Returns the index of the model name in the EXPLICIT_MODEL_ORDER list.
    Models not in the list will be assigned a high index, sorting them last.
    """
    try:
        return EXPLICIT_MODEL_ORDER.index(model_name_for_sorting)
    except ValueError:
        # If model_name_for_sorting is not in the explicit list, sort it last alphabetically.
        # This sorts unlisted models among themselves based on their name.
        # This ensures stable ordering even if new models appear in data not in explicit list.
        return len(EXPLICIT_MODEL_ORDER) + 1


def main():
    os.makedirs(OUTPUT_PLOTS_DIRECTORY, exist_ok=True)

    all_judgments_data = []
    for filename in os.listdir(JUDGMENTS_DIRECTORY):
        if filename.endswith(".json") and filename.startswith("judgment_"):
            filepath = os.path.join(JUDGMENTS_DIRECTORY, filename)
            judgment = parse_judgment_file(filepath)
            if judgment:
                all_judgments_data.append(judgment)

    if not all_judgments_data:
        print(
            f"No judgment files found or parsed in '{JUDGMENTS_DIRECTORY}'. Please ensure files exist and are correctly formatted.")
        return

    df = pd.DataFrame(all_judgments_data)

    # Convert user_prompt_index to integer
    df['user_prompt_index'] = pd.to_numeric(df['user_prompt_index'], errors='coerce').fillna(-1).astype(int)
    df.dropna(subset=['user_prompt_index'], inplace=True)  # Drop rows where prompt index is NaN
    df = df[df['user_prompt_index'] != -1]  # Filter out unparseable prompts

    # Add a new column for 1-indexed user prompt for plotting
    df['user_prompt_display_index'] = df['user_prompt_index'] + 1

    # Apply the display formatting to the model names
    df['evaluated_model_display_name'] = df['evaluated_model_name'].apply(_format_for_display)

    # --- Print for debugging (kept for verification) ---
    print("\n--- Unique Formatted Model Names Found in Data ---")
    for name in sorted(df['evaluated_model_display_name'].unique()):
        print(f"- '{name}'")
    print("---------------------------------------------------\n")
    # --- End Debugging Print ---

    # Convert total_rating to numeric
    df['total_rating'] = pd.to_numeric(df['total_rating'], errors='coerce')
    df.dropna(subset=['total_rating'], inplace=True)  # Drop rows where rating is NaN

    # Determine unique judge and reference info for plot title (using original names from JSON)
    unique_judge_models = df['judge_model'].unique()
    unique_judge_temps = df['judge_temperature'].unique()
    unique_ref_model_names = df['ref_file_path'].apply(get_ref_model_name).unique()

    judge_info = f"Judge: {', '.join(unique_judge_models)} (Temp: {', '.join(map(str, unique_judge_temps))})"
    reference_info = f"Reference: {', '.join(unique_ref_model_names)}"

    # Filter `ordered_evaluated_models` to only include models actually present in the dataframe,
    # while maintaining the order from EXPLICIT_MODEL_ORDER.
    unique_models_in_data = df['evaluated_model_display_name'].unique()
    ordered_evaluated_models = [
        model for model in EXPLICIT_MODEL_ORDER if model in unique_models_in_data
    ]

    # Add any models present in the data but NOT in EXPLICIT_MODEL_ORDER to the end, alphabetically
    remaining_models = sorted([
        model for model in unique_models_in_data if model not in EXPLICIT_MODEL_ORDER
    ])
    ordered_evaluated_models.extend(remaining_models)

    print(f"\nFound data for {len(df['user_prompt_display_index'].unique())} user prompts.")
    print(f"Evaluated models (ordered for plot):")
    for model in ordered_evaluated_models:
        print(f"- {model}")  # Print sorted list for verification
    print(f"Judge info: {judge_info}")
    print(f"Reference info: {reference_info}")

    # Plotting for each user prompt separately (existing logic)
    for prompt_idx_0_indexed in sorted(df['user_prompt_index'].unique()):
        prompt_df = df[df['user_prompt_index'] == prompt_idx_0_indexed].copy()
        user_prompt_display_index = prompt_idx_0_indexed + 1  # Use the 1-indexed value for display

        if prompt_df.empty:
            print(f"No data for user prompt {prompt_idx_0_indexed}. Skipping plot.")
            continue

        plt.figure(figsize=(14, 8))

        bar_plot = sns.barplot(
            data=prompt_df,
            x='evaluated_model_display_name',
            y='total_rating',
            hue='evaluated_model_temp',
            palette='viridis',
            errorbar='sd',  # Standard deviation error bars
            capsize=0.1,
            order=ordered_evaluated_models
        )

        plt.title(f'Total Rating for User Prompt {user_prompt_display_index}\n{judge_info}, {reference_info}')
        plt.xlabel('Evaluated Model')
        plt.ylabel(f'Average Total Rating (Scale {EXPECTED_RATING_RANGE[0]}-{EXPECTED_RATING_RANGE[1]})')
        plt.ylim(EXPECTED_RATING_RANGE[0] - 0.1, EXPECTED_RATING_RANGE[1] + 0.1)
        plt.yticks(range(EXPECTED_RATING_RANGE[0], EXPECTED_RATING_RANGE[1] + 1))

        plt.xticks(rotation=45, ha='right')

        for container in bar_plot.containers:
            bar_plot.bar_label(container, fmt='%.2f', label_type='edge', padding=3)

        plt.legend(title='Evaluated Model Temp', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout(rect=[0, 0, 0.88, 1])
        plot_filename = os.path.join(OUTPUT_PLOTS_DIRECTORY, f'total_rating_userprompt_{user_prompt_display_index}.png')
        plt.savefig(plot_filename)
        plt.close()
        print(f"Plot saved for User Prompt {user_prompt_display_index}: {plot_filename}")

    # --- NEW: Overall Average Rating Plot for All Prompts ---
    print("\nGenerating overall average rating plot...")

    # We use the full 'df' here so that seaborn's barplot can calculate
    # the mean and standard deviation from the underlying data correctly.
    plt.figure(figsize=(14, 8))

    overall_bar_plot = sns.barplot(
        data=df,  # <--- CHANGED FROM overall_avg_df BACK TO THE FULL DF
        x='evaluated_model_display_name',
        y='total_rating',
        hue='evaluated_model_temp',
        palette='viridis',
        errorbar='sd',  # <--- THIS WILL NOW CORRECTLY SHOW STANDARD DEVIATION
        capsize=0.1,
        order=ordered_evaluated_models  # Use the same explicit order
    )

    plt.title(f'Overall Average Total Rating Across All Prompts (1-8)\n{judge_info}, {reference_info}')
    plt.xlabel('Evaluated Model')
    plt.ylabel(f'Overall Average Total Rating (Scale {EXPECTED_RATING_RANGE[0]}-{EXPECTED_RATING_RANGE[1]})')
    plt.ylim(EXPECTED_RATING_RANGE[0] - 0.1, EXPECTED_RATING_RANGE[1] + 0.1)
    plt.yticks(range(EXPECTED_RATING_RANGE[0], EXPECTED_RATING_RANGE[1] + 1))

    plt.xticks(rotation=45, ha='right')

    for container in overall_bar_plot.containers:
        overall_bar_plot.bar_label(container, fmt='%.2f', label_type='edge', padding=3)

    plt.legend(title='Evaluated Model Temp', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    overall_plot_filename = os.path.join(OUTPUT_PLOTS_DIRECTORY, 'overall_total_rating_all_prompts.png')
    plt.savefig(overall_plot_filename)
    plt.close()
    print(f"Overall average rating plot saved: {overall_plot_filename}")

    print("\nAll plots generated successfully.")


if __name__ == "__main__":
    main()