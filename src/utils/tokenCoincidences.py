import pandas as pd

def match_tokens(input_dataframe, token_dataframes):
    # Create a new column in the input dataframe which is the concatenation of 'lemma' and 'pos'
    input_dataframe['lemma_pos'] = input_dataframe['lemma'] + '_' + input_dataframe['pos']
    # Convert dataframe lemmas into a set (to remove duplicates)
    input_lemmas_pos = set(input_dataframe['lemma_pos'].dropna())
    total_input_lemmas_pos = len(input_lemmas_pos)

    matching_results = {}
    total_matching_lemmas_pos = 0

    # Iterate through each toke_dataframes in the dataframe
    for file_name, df in token_dataframes.items():
        # Create a new column in the current dataframe which is the concatenation of 'lemma' and 'pos'
        df['lemma_pos'] = df['lemma'] + '_' + df['pos']
        # Convert current dataframe lemmas into a set (to remove duplicates)
        token_lemmas_pos = set(df['lemma_pos'].dropna())
        # Find the intersection of both sets (lemmas which are in both sets)
        matching_lemmas_pos = input_lemmas_pos & token_lemmas_pos
        num_matching_lemmas_pos = len(matching_lemmas_pos)
        total_matching_lemmas_pos += num_matching_lemmas_pos
        # Calculate the percentage of lemma matching
        percentage_matching_lemmas_pos = (num_matching_lemmas_pos / total_input_lemmas_pos) * 100
        matching_results[file_name] = (num_matching_lemmas_pos, percentage_matching_lemmas_pos)
        print(f'{file_name}')
        print(f'\tTotal matching: {num_matching_lemmas_pos} - {percentage_matching_lemmas_pos:.2f}%')
        # Remove matching lemmas from input_lemmas_pos to not count them multiple times
        input_lemmas_pos -= matching_lemmas_pos

    # Calculate the total percentage of matching lemmas
    total_percentage_matching = (total_matching_lemmas_pos / total_input_lemmas_pos) * 100
    print(f'Total matching: {total_matching_lemmas_pos} - {total_percentage_matching:.2f}%')

def match_lemmas(input_dataframe, vocabulary_dataframes):
    input_lemmas = input_dataframe['lemma']
    total_matching_hiragana = 0
    total_matching_kanji = 0
    
    for file_name, df in vocabulary_dataframes.items():
        matching_kanji = []
        matching_hiragana = []
        
        kanji_lemmas = df['Kanji'].dropna()
        hiragana_lemmas = df['Hiragana'].dropna()
        
        matching_kanji.extend(input_lemmas[input_lemmas.isin(kanji_lemmas)])
        num_matching_kanji = len(matching_kanji)
        total_matching_kanji += num_matching_kanji
        
        matching_hiragana.extend(input_lemmas[input_lemmas.isin(hiragana_lemmas)])
        num_matching_hiragana = len(matching_hiragana)
        total_matching_hiragana += num_matching_hiragana
        
        percentage_matching_kanji = (num_matching_kanji / len(input_lemmas)) * 100
        percentage_matching_hiragana = (num_matching_hiragana / len(input_lemmas)) * 100
        
        print(f'{file_name}')
        print(f'\tTotal matching Kanji: {num_matching_kanji} - {percentage_matching_kanji:.2f}%')
        print(f'\tTotal matching Hiragana: {num_matching_hiragana} - {percentage_matching_hiragana:.2f}%')
        print(f'\tTotal cumulative matching in this file: {num_matching_kanji + num_matching_hiragana} - {(percentage_matching_kanji + percentage_matching_hiragana):.2f}%')
    
    total_unique_matching_kanji = len(set(input_lemmas[input_lemmas.isin(pd.concat([df['Kanji'] for df in vocabulary_dataframes.values()]).dropna())]))
    total_unique_matching_hiragana = len(set(input_lemmas[input_lemmas.isin(pd.concat([df['Hiragana'] for df in vocabulary_dataframes.values()]).dropna())]))
    
    print(f'Total unique matching Kanji: {total_unique_matching_kanji} - {(total_unique_matching_kanji / len(input_lemmas)) * 100:.2f}%')
    print(f'Total unique matching Hiragana: {total_unique_matching_hiragana} - {(total_unique_matching_hiragana / len(input_lemmas)) * 100:.2f}%')


def match_vocabulary(input_dataframe, vocabulary_dataframes, language_level):
    # Set display options to show all rows on print results
    pd.set_option('display.max_rows', None)
    matching_tokens = {}

    # Define the language levels in order
    language_levels = ['N5', 'N4', 'N3', 'N2', 'N1']

    for filename, vocabulary_df in vocabulary_dataframes.items():
        # Get Level from file_name the filename is in the two first characters
        # Example: n5Vocab.csv -> level = 'N5'
        level = filename[:2].upper()

        # Get the input_dataframe lemma column
        input_lemmas = input_dataframe['lemma']

        # Check if the level is higher than the language_level provided
        if language_levels.index(level) > language_levels.index(language_level.upper()):
            # Get the kanji column
            kanji_list = vocabulary_df['Kanji']
            # Get the hiragana column
            hiragana_list = vocabulary_df['Hiragana']

            # If input_lemmas contains any of the kanji_list or hiragana_list save all the row in a new dataframe
            matching_kanji = input_lemmas[input_lemmas.isin(kanji_list)]
            matching_hiragana = input_lemmas[input_lemmas.isin(hiragana_list)]

            # Save the matching rows in a new dataframe if there are any matches with kanji or hiragana
            matching_rows = vocabulary_df[
                (vocabulary_df['Kanji'].isin(matching_kanji)) |
                (vocabulary_df['Hiragana'].isin(matching_hiragana))
            ]

            # Save the matching rows in the matching_tokens dictionary with the level as key
            if not matching_rows.empty:
                matching_tokens[level] = matching_rows
    
    matching_tokens_by_level = {}


    # Display each level matching tokens
    if matching_tokens:
        for level, matching_tokens_df in matching_tokens.items():
            # Save the matching tokens by level in a dictionary
            matching_tokens_by_level[level] = matching_tokens_df
            # Print the level and the vocabulary and save it in a csv file
            print(f'\n{level} vocabulary:\n')
            print(matching_tokens_df.to_string(index=False))  # Print DataFrame without index
    else:
        print(f'No vocabulary found higher than {language_level} in the input text.')

    return matching_tokens_by_level
