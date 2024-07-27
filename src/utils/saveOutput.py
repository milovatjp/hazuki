import os
import pandas as pd

# Save output text in JSON format
def save_output_json(data, output_file_path):
    try:
      data_cf = pd.json_normalize(data)
    except ValueError:
      data_cf = pd.json_normalize([data])

    # check if the file exists and ask if the user wants to overwrite it if not ask for a new file name
    if os.path.exists(output_file_path):
        print("The file already exists. Do you want to overwrite it? (y/n): ")
        if input().lower() == 'n':
            print("Please provide a new file name.")
            output_file_path = input("Please provide the name of the file to save the matched vocabulary data: ")
        elif input().lower() == 'y':
            print("Overwriting the file.")
    try:
        # Add the .json extension to the file if it doesn't have it
        if not output_file_path.endswith('.json'):
            output_file_path += '.json'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            data_cf.to_json(output_file, orient='records', lines=True, force_ascii=False)

        print(f"Processed text saved to '{output_file_path}'")
    except Exception as e:
        print("Error saving the file: ", {e})

# Save output text in CSV format
def save_output_csv(data, output_file_path):
    try:
        data_df = pd.DataFrame(data)
    except ValueError:
        data_df = pd.DataFrame([data])
    # check if the file exists and ask if the user wants to overwrite it if not ask for a new file name
    if os.path.exists(output_file_path):
        print("The file already exists. Do you want to overwrite it? (y/n): ")
        if input().lower() == 'n':
            print("Please provide a new file name.")
            output_file_path = input("Please provide the name of the file to save the matched vocabulary data: ")
        elif input().lower() == 'y':
            print("Overwriting the file.")
    try:
        # Add the .csv extension to the file if it doesn't have it
        if not output_file_path.endswith('.csv'):
            output_file_path += '.csv'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            data_df.to_csv(output_file, index=False)

        print(f"Processed text saved to '{output_file_path}'")
    except Exception as e:
        print("Error saving the file: ", {e})