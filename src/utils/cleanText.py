import re

def remove_unicode(text):
  # Remove all unicode characters
  text = re.sub(r'[\ufffa\ufffb\ufffd\ufff9\u3000\u00a9]', '', text)

  return text

def remove_alphanumeric(text):
  # Remove all alphanumeric characters and spaces
  text = re.sub(r'[a-zA-Z0-9 ]', '', text)

  return text

def remove_line_feeds(text):
  # Remove all existing line feeds
  text = text.replace('\n', '')

  return text

def insert_line_feeds_after_dot_space(text):
  # Insert a line feed after every occurrence of "。"
  text = text.replace('。', '。\n')

  return text

def clean_text(text):
  text = remove_unicode(text)
  text = remove_alphanumeric(text)
  text = remove_line_feeds(text)
  text = insert_line_feeds_after_dot_space(text)

  return text

def save_clean_text_file(input_file_path, output_file_path):
  try:
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
      for line in input_file:
        processed_line = clean_text(line)
        output_file.write(processed_line)

    print(f"Processed text saved to '{output_file_path}'")
  except FileNotFoundError: 
    print("File not found.")
