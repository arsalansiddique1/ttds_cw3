from mwparserfromhtml import HTMLDump
import csv
import re
from itertools import filterfalse
from nltk.stem import PorterStemmer

html_file_path = "/Users/Ivibae/enwiki-NS0-20240201-ENTERPRISE-HTML.json.tar.gz"
html_dump = HTMLDump(html_file_path)

csv_file_path = 'try.csv'


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
    return stopwords

def preprocess_text(text, stopwords):
    '''
    Preprocess a single text: tokenization, stopping, case folding, stemming
    '''
    tokens = re.findall(r'\b[\w\']+\b', re.sub(r'_', ' ', text).lower())
    tokens = list(filterfalse(stopwords.__contains__, tokens)) 
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

image_id = 0


stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:

    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['title', 'filenames', 'image id', 'captions'])

    for article in html_dump:
        title = article.get_title()
        for image in article.html.wikistew.get_images():

            if image.caption != "":     #only include images with a caption
                filename = image.title
            
                cleaned_caption = preprocess_text(image.caption, stopwords)
                csv_writer.writerow([title, filename, image_id, ' '.join(cleaned_caption)])
                print(f'Filename: {filename}, Caption: {image.caption}')
                image_id += 1

        if image_id == 10000:
            break
