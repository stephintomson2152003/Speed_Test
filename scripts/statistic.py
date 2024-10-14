import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

# Load input history data from the local storage file (JSON format for example purposes)
def load_input_history(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                # Convert dict to list if needed (e.g., a single input record as a dict)
                data = [data]
            elif not isinstance(data, list):
                raise ValueError("Input history is not a list or a valid dictionary.")
            if len(data) == 0:
                raise ValueError("Input history is empty.")
            # Ensure each entry has a timestamp, add if missing
            for entry in data:
                if 'timestamp' not in entry:
                    entry['timestamp'] = datetime.datetime.now().isoformat()
            return data
    except FileNotFoundError:
        raise ValueError(f"The file '{filename}' does not exist. Please make sure it is available in the correct directory.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{filename}' is not a valid JSON. Please correct its format.")

# Calculate input speed (keys per minute)
def calculate_input_speed(input_history):
    if not input_history:
        return 0
    start_time = datetime.datetime.fromisoformat(input_history[0].get('timestamp'))
    end_time = datetime.datetime.fromisoformat(input_history[-1].get('timestamp'))
    duration_minutes = (end_time - start_time).total_seconds() / 60
    return len(input_history) / duration_minutes if duration_minutes > 0 else 0

# Calculate accuracy
def calculate_accuracy(current_sentence, user_input):
    correct_chars = sum(1 for i in range(min(len(current_sentence), len(user_input))) if current_sentence[i] == user_input[i])
    return (correct_chars / len(current_sentence)) * 100 if len(current_sentence) > 0 else 0

# Calculate words per minute based on correct words entered
def calculate_words_per_minute(input_history, current_sentence, user_input):
    if not input_history:
        return 0
    start_time = datetime.datetime.fromisoformat(input_history[0].get('timestamp'))
    end_time = datetime.datetime.fromisoformat(input_history[-1].get('timestamp'))
    duration_minutes = (end_time - start_time).total_seconds() / 60
    correct_words = sum(1 for word1, word2 in zip(current_sentence.split(), user_input.split()) if word1 == word2)
    return correct_words / duration_minutes if duration_minutes > 0 else 0

# Calculate raw statistics (correct, incorrect, missed characters)
def calculate_raw_statistics(current_sentence, user_input):
    correct = sum(1 for i in range(min(len(current_sentence), len(user_input))) if current_sentence[i] == user_input[i])
    incorrect = sum(1 for i in range(min(len(current_sentence), len(user_input))) if current_sentence[i] != user_input[i])
    missed = len(current_sentence) - len(user_input) if len(user_input) < len(current_sentence) else 0
    return {"correct": correct, "incorrect": incorrect, "missed": missed}

# Plot graphs for statistics and save them as images
def plot_statistics(input_history, current_sentence, user_input):
    if not input_history:
        print("No input history available to plot statistics.")
        return

    input_speed = calculate_input_speed(input_history)
    accuracy = calculate_accuracy(current_sentence, user_input)
    words_per_minute = calculate_words_per_minute(input_history, current_sentence, user_input)
    raw_stats = calculate_raw_statistics(current_sentence, user_input)

    # Plotting graph similar to Monkeytype's WPM and errors graph
    time_points = list(range(1, len(input_history) + 1))
    wpm_values = [words_per_minute] * len(input_history)  # Simulating consistency
    error_values = [raw_stats["incorrect"]] * len(input_history)  # Fixed error count

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Time Points')
    ax1.set_ylabel('Words per Minute', color='yellow')
    ax1.plot(time_points, wpm_values, color='yellow', label='WPM', linewidth=2)
    ax1.tick_params(axis='y', labelcolor='yellow')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Errors', color='red')
    ax2.plot(time_points, error_values, 'r-', label='Errors', marker='x')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.tight_layout()

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the plot as an image
    output_path = os.path.join(output_dir, 'statistics.png')
    plt.savefig(output_path)
    plt.close()

    print(f"Statistics graph saved at {output_path}")

    # Save statistics data
    stats = {
        "input_speed": input_speed,
        "accuracy": accuracy,
        "words_per_minute": words_per_minute,
        "raw_statistics": raw_stats
    }
    stats_path = os.path.join(output_dir, 'statistics.json')
    with open(stats_path, 'w') as stats_file:
        json.dump(stats, stats_file, indent=2)
    print(f"Statistics data saved at {stats_path}")

if __name__ == "__main__":
    # Example: Load input history and current game data
    try:
        input_history = load_input_history('../input_history.json')
        current_sentence = "The quick brown fox jumps over the lazy dog"
        user_input = "The quack brown fox jumps over the lazy dog"

        plot_statistics(input_history, current_sentence, user_input)
    except ValueError as e:
        print(f"Error: {e}")