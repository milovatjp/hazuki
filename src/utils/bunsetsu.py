import spacy
import ginza

nlp = spacy.load('ja_ginza_electra')

from collections import Counter

def count_bunsetsu(text: str):
    bunsetsu_list = []
    bunsetsu_count_per_sentence = Counter()
    bunsetsu_results = []

    sentences = text.split('\n')  # Split by "。" to get sentences
    for sentence in sentences:
        if sentence.strip():  # Check if the sentence is not empty
            try:
                doc = nlp(sentence)
            except Exception as e:
                print(f"Error processing sentence: {sentence}. Error: {e}")
                continue

            bunsetsu = ginza.bunsetu_spans(doc)
            bunsetsu_list.append(bunsetsu)

            bunsetsu_count = len(list(ginza.bunsetu_spans(doc)))
            bunsetsu_count_per_sentence[sentence] = bunsetsu_count

            bunsetsu_results.append({
                'Sentence': sentence,
                'List of Bunsetsu': bunsetsu,
                'Bunsetsu Count': bunsetsu_count
            })

    return bunsetsu_results


if __name__ == "__main__":
    # Input file
    input_file = '../../data/news/news_clean.txt'

    # Open the input file, read the content, and extract the bunsetsu
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    count_bunsetsu(text)