import re

def count_kanji(text):
  text_length = len(text)
  # Kanji Unicode range: \u4e00-\u9faf
  kanji_pattern = re.compile(r'[\u4e00-\u9faf]')

  # Find all kanji characters in the text
  kanji_characters = kanji_pattern.findall(text)
  kanji_characters_len = len(kanji_characters)
  kanji_characters_percentage = (kanji_characters_len / text_length) * 100

  # Return the number of kanji characters
  print(f"The text length is: {text_length} characters and the number of kanji characters is: {kanji_characters_len} - {kanji_characters_percentage:.2f}% of the text")

def count_hiragana(text):
  text_length = len(text)
  # Hiragana Unicode range: \u3040-\u309f
  hiragana_pattern = re.compile(r'[\u3040-\u309f]')

  # Find all hiragana characters in the text
  hiragana_characters = hiragana_pattern.findall(text)
  hiragana_characters_len = len(hiragana_characters)
  hiragana_characters_percentage = (hiragana_characters_len / text_length) * 100

  # Return the number of hiragana characters
  print(f"The text length is: {text_length} characters and the number of hiragana characters is: {hiragana_characters_len} - {hiragana_characters_percentage:.2f}% of the text")


if __name__ == "__main__":
    # Input text with kanjis
    input_kanji_text = "私は日本語を勉強しています。123 ABC"
    # Input text with hiraganas
    input_hiragana_text = "ひらがなを勉強しています。123 ABC"

    # Count the number of kanji characters
    kanji_count = count_kanji(input_kanji_text)
    print(f"Number of kanji characters: {kanji_count}") # Output: 6

    # Count the number of hiragana characters
    hiragana_count = count_hiragana(input_hiragana_text)
    print(f"Number of hiragana characters: {hiragana_count}") # Output: 10
