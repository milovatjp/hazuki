from .cleanText import clean_text
import os
import glob
import pandas as pd

def read_json_files(path: str):
    files = sorted(glob.glob(path))
    dataframes = {os.path.basename(file): pd.read_json(file) for file in files}
    return dataframes

def read_csv_files(path: str):
    files = sorted(glob.glob(path))
    dataframes = {os.path.basename(file): pd.read_csv(file) for file in files}
    return dataframes

def process_file(input_file_path, output_file_path):
  try:
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
      for line in input_file:
        processed_line = clean_text(line)
        output_file.write(processed_line)

    print(f"Processed text saved to '{output_file_path}'")
  except FileNotFoundError: 
    print("File not found.")