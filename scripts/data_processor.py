# scripts/data_processor.py
import sys
import json
import random

def process_data(data):
    # Example: Reverse the input string
    return data[::-1]

def get_random_sentence():
    try:
        with open('sentences.txt', 'r') as file:
            sentences = [line.strip() for line in file if line.strip()]
        return random.choice(sentences)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'get_sentence':
        # Get a random sentence from sentences.txt
        random_sentence = get_random_sentence()
        print(json.dumps({"sentence": random_sentence}))
    else:
        # Process the provided data
        input_data = sys.argv[1]
        processed_data = process_data(input_data)
        print(json.dumps({"result": processed_data}))
