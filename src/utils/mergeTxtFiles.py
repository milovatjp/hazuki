import os
import re

def merge_txt_files(input_dir, output_file):
  # Get a sorted list of filenames in the directory
  files = sorted(os.listdir(input_dir), key=lambda x: int(re.findall(r'\d+', x)[0]))
  
  with open(output_file, 'w') as outfile:
    for filename in files:
      if filename.endswith(".txt"):
        with open(os.path.join(input_dir, filename), 'r') as infile:
          outfile.write(infile.read())
          outfile.write('\n')  # Add a newline between files