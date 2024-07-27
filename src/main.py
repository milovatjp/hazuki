# src/main.py
import sys
import os
import pandas as pd
import json
from utils import clean_text, count_bunsetsu, count_hiragana, count_kanji, match_lemmas, match_tokens, match_vocabulary, read_csv_files, read_json_files, save_clean_text_file, tokenize_text, save_output_json, save_output_csv

def main():

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Read the token dataframes
    token_dataframes_path = os.path.join(script_dir, '../data/tokens/*.json')
    token_dataframes = read_json_files(token_dataframes_path)
    vocabulary_dataframes_path = os.path.join(script_dir, '../data/vocabulary/*.csv')
    vocabulary_dataframes = read_csv_files(vocabulary_dataframes_path)

    # Welcome message to the user
    print("Welcome to the Text Processing Tool!")
    print("This tool will clean and tokenize your text files.")

    # Wait until the user provides the input file
    while True:
        input_file_path = input("Please provide the input file with the text to process: ")
        if input_file_path:
            break
        print("Please provide the input file: ")
    
    # Get the input file path
    print(f"Input file: {input_file_path}")

    # Read the input file
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)

    # Clean and tokenize the text
    processed_text = clean_text(text)
    tokenized_text = tokenize_text(processed_text)
    input_dataframe = pd.json_normalize(tokenized_text)

    # Ask the user for the japanese level that he/she has by default is N5
    print("\nWhat is your Japanese knowleged level? If you don't provide it, it will default to N5.")
    japanese_level = input("Please provide your Japanese level (N5, N4, N3, N2, N1): ").upper() or "N5"
    if japanese_level not in ["N5", "N4", "N3", "N2", "N1"]:
        print("The format is not correct. Would you like to try again? (y/n): ")
        if input().lower() == 'y':
            japanese_level = input("Please provide your Japanese level (N5, N4, N3, N2, N1): ")
        elif input().lower() == 'n':
                print("Using the default level N5.")
    elif japanese_level:
        print(f"Your Japanese level is: {japanese_level}")

    # Print a menu with the options for the user
    while True:
        print("\nYou can choose one of the following options:")
        print("\t1. Compare the tokenized text with a list of tokens.")
        print("\t2. Compare the tokenized text with a list of vocabulary.")
        print("\t3. Count the number of bunsetsu in the text.")
        print("\t4. Get the number of Kanjis and Hiragana characters in the text.")
        print("\t5. Exit the program.")
        option = input("Please choose an option: ")

        if option == "1":
            print("\n---------------------")
            match_tokens(input_dataframe, token_dataframes)
            print("---------------------")

        elif option == "2":
            print("\n---------------------")
            match_lemmas(input_dataframe, vocabulary_dataframes)
            vocabulary_option = input("Do you want to get the vocabulary higher that the level you provided? (y/n): ")
            if vocabulary_option.lower() == 'y':
                print("Getting the vocabulary higher than your level.")
                vocabulary_match = match_vocabulary(input_dataframe, vocabulary_dataframes, japanese_level)

                # Ask the user if want to save the match_vocabulary data into a file
                save_option = input("Do you want to save the matched vocabulary data into a file? (y/n): ")
                if save_option.lower() == 'y':
                    # Ask the user for the file name
                    save_file_name = input("Please provide the name of the file to save the matched vocabulary data: ")
                    # Ask the user if want JSON file or CSV file and send the match_vocabulary data to the corresponding function
                    save_file_format = input("Please provide the format of the file (json or csv): ")
                    if save_file_format.lower() == 'json':
                        save_output_json(vocabulary_match, save_file_name)
                    elif save_file_format.lower() == 'csv':
                        save_output_csv(vocabulary_match, save_file_name)
                    else:
                        print("The format is not correct. Please try again.")
            print("---------------------")

        elif option == "3":
            print("\n---------------------")
            bunsetsu_data = count_bunsetsu(processed_text)
            for item in bunsetsu_data:
                print(f"Sentence: {item.sentence}")
                print(f"List of Bunsetsu: {item.bunsetsu}")
                print(f"Bunsetsu count: {item.bunsetsu_count}\n")

            # Ask the user if want to save the count_bunsetsu data into a file
            save_option = input("Do you want to save the count bunsetsu data into a file? (y/n): ")
            if save_option.lower() == 'y':
                # Ask the user for the file name
                save_file_name = input("Please provide the name of the file to save the matched vocabulary data: ")
                # Add the txt extension to the file if it doesn't have it
                if not save_file_name.endswith('.txt'):
                    save_file_name += '.txt'
                # save the count_buntsetsu data into a txt file
                with open(save_file_name, 'w', encoding='utf-8') as output_file:
                    for item in bunsetsu_data:
                        output_file.write(f"Sentence: {item['Sentence']}\n")
                        bunsetsu_str_list = [str(span) for span in item['List of Bunsetsu']]
                        output_file.write("List of Bunsetsu: " + ', '.join(bunsetsu_str_list) + "\n")
                        output_file.write(f"Bunsetsu Count: {item['Bunsetsu Count']}\n")
                        output_file.write("\n")
            print("---------------------")

        elif option == "4":
            print("\n---------------------")
            count_hiragana(processed_text)
            count_kanji(processed_text)
            print("---------------------")

        elif option == "5":
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()