import sys

from mwparserfromhtml import HTMLDump
import re
from itertools import filterfalse
from nltk.stem import PorterStemmer
from tqdm import tqdm

html_file_path = sys.argv[1]
html_dump = HTMLDump(html_file_path)

import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()


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

with db.connect() as conn:

    stmt = sqlalchemy.text(
        "INSERT INTO captions (id, filename, title, caption) VALUES (:id, :filename, :title, :caption)"
    )

    for article in tqdm(html_dump):
        title = article.get_title()
        for image in article.html.wikistew.get_images():

            if image.caption != "":     #only include images with a caption
                filename = image.title

                cleaned_caption = ' '.join(preprocess_text(image.caption, stopwords))

                conn.execute(stmt, parameters=
                    {"id": image_id, "filename": filename, "title": title, "caption": cleaned_caption}
                )
                conn.commit()

                image_id += 1

        # if image_id == 10000:
        #     break
