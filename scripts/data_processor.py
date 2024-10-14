# scripts/data_processor.py
import sys
import json

def process_data(data):
    # Example: Reverse the input string
    return data[::-1]

if __name__ == "__main__":
    input_data = sys.argv[1]
    processed_data = process_data(input_data)
    print(json.dumps({"result": processed_data}))
