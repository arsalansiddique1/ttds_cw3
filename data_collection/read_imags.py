from itertools import filterfalse
import re
import csv
import string
from nltk.stem import PorterStemmer


file_path = 'enwiki-latest-pages-articles1.xml-p1p41242/short.xml'

image_pattern = re.compile(r'\[\[File:(.*?)\]\]')

csv_file_path = 'images_with_captions.csv'

with open(file_path, 'r', encoding='utf-8') as file, \
     open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filenames', 'captions'])

    for line in file:
        matches = image_pattern.findall(line)
        for match in matches:
            # Split the match into filename and the rest of the content
            parts = match.split('|', 1)
            filename = parts[0]
            #caption = parts[1] if len(parts) > 1 else ''
            # Write to the CSV file
            stopwords = extract_stopwords(ttds_2023_english_stop_words.txt)
            cleaned_line = preprocess_text(line, stopwords)
            csv_writer.writerow([filename, cleaned_line.strip()])
            #print(f'Filename: {filename}, Caption: {caption}')
            


def extract_stopwords(stopwords_file):
    '''
    Helper function to extract stopwords from a stopwords file
    '''
    if stopwords_file is None:
        return []
    with open(stopwords_file, 'r', encoding="utf-8") as s:
        text = s.read().lower()
        pattern = r'\b[\w\']+\b'
        stopwords = re.findall(pattern, text)
    print('There are', len(stopwords), 'stopwords to remove.')
    return stopwords

def preprocess_text(text, stopwords):
    '''
    Preprocess a single text: tokenization, stopping, case folding, stemming
    '''
    tokens = re.findall(r'\b[\w\']+\b', text.lower())
    tokens = list(filterfalse(stopwords.__contains__, tokens))
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


# def preprocess_data(line):
#     chars_to_remove = re.compile(f'[{string.punctuation}]')
    
#     tweet_texts = []
#     categories = []
#     unique_words = set([])
        
#     line = line.strip()
#     if line:
#         tweet_id, category, tweet_text = line.split('\t')
#         words = chars_to_remove.sub('',tweet_text).lower().split()
        
#         for word in words:
#             unique_words.add(word)   
            
#         tweet_texts.append(words)
#         categories.append(category)
            
#     return tweet_texts, categories, unique_words