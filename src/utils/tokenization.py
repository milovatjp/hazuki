import os
import spacy
import json

nlp = spacy.load('ja_ginza_electra')

def tokenize_text(text: str, max_length=49149):
    # Divide the text into segments of a maximum length. Ginza cannot process texts over 49149 bytes
    segments = []
    segment = ''
    
    # Split the text into segments of a maximum length of bytes (49149) to avoid Ginza errors
    for word in text.split():
      if len((segment + word).encode('utf-8')) > max_length:
        segments.append(segment)
        segment = word + ' '
      else:
        segment += word + ' '
    segments.append(segment)
    
    # Tokenize each segment
    tokens = set()
    # Iterate over the segments and tokenize them with Ginza
    for i, segment in enumerate(segments):
      doc = nlp(segment)
      # Add the tokens to the set of tokens (to avoid duplicates)
      tokens.update(tuple(token.items()) for token in [
        {
          'text': token.text,
          'norm': token.norm_,
          'pos': token.pos_,
          'lemma': token.lemma_
        } for token in doc
      ])
      
      # Print the progress percentage
      print(f'Completed: {(i + 1) / len(segments) * 100:.2f}%', end='\r')
    
    # Return the set of tokens as a list of dictionaries (to be JSON serializable)
    return [dict(t) for t in tokens]

def save_tokenize_text(input_file: str, output_extension: str):
  # Open the input file, read the content, and tokenize the content
  with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()
    
  tokens = tokenize_text(text)
  
  # Save the tokens to a TXT output file
  if (output_extension == "txt"):
    output_file = os.path.splitext(input_file)[0] + "_tokenized." + output_extension
    with open(output_file, 'w', encoding='utf-8') as f:
      for token in tokens:
        f.write(f"{token[0]} {token[1]} {token[2]}\n")
    
  # Save the tokens to a JSON output file
  elif (output_extension == "json"):
    output_file = os.path.splitext(input_file)[0] + "." + output_extension
    with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(tokens, f, ensure_ascii=False, indent=4)

  # If format is not correct, print an error message
  else:
    print("Output format not valid. Use 'txt' or 'json' as the second argument.")

  print(f"Tokenized text saved to '{output_file}'")
