import argparse
import os
import glob
from .tokenization import save_tokenize_text
from .cleanText import save_clean_text_file

# Used to tokenize and save the batch of files of tokens and vocabulary
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tokenize and save text.')
    parser.add_argument('input_directory', type=str, help='The directory of input files to tokenize.')
    parser.add_argument('output_directory', type=str, help='The directory to save the tokenized files.')
    parser.add_argument('output_extension', type=str, help='The extension of the output file.')
    args = parser.parse_args()
    
    # Check if output directory exists, create it if it doesn't
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
        
    files = sorted(glob.glob(args.input_directory + '/*.txt'))
    for file in files:
        # Get the filename without the extension
        base_filename = os.path.splitext(os.path.basename(file))[0]
        # Get the full path to the cleaned output file
        output_file_path = os.path.join(args.output_directory, base_filename + '.txt')
        print('Clean ' + file)
        # Clean the file
        save_clean_text_file(file, output_file_path)
        # Get the full path to the tokenized output file
        input_file_path = os.path.join(args.output_directory, base_filename + '.txt')
        print('Tokenize ' + input_file_path + ' to ' + args.output_extension)
        # Tokenize the file and save it
        save_tokenize_text(input_file_path, args.output_extension)
