import csv
import re
from nltk.stem import PorterStemmer
from itertools import filterfalse
import string

# Moving the stopwords, tokenisation and stemming from caption_extraction to indxing
# Take UNPROCESSED caption and PROCESS it
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


# def preprocess_text(text, stopwords):
#     '''
#     Preprocess a single text: tokenization, stopping, case folding, stemming
#     '''
#     text_np = "".join([i for i in text if i not in string.punctuation]) # punctuation removal
#     tokens = re.findall(r'\b[\w\']+\b', re.sub(r'_', ' ', text_np).lower())
#     tokens = list(filterfalse(stopwords.__contains__, tokens)) 
#     stemmer = PorterStemmer()
#     return [stemmer.stem(token) for token in tokens]

def preprocess_text(text, stopwords):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = text.split()
    stemmer = PorterStemmer()
    tokens = [
        stemmer.stem(token) for token in tokens if token.lower() not in stopwords
    ]
    return tokens


# Reading the csv file
def read_csv_file(file_path, stopwords):
    text_dict = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            file = row['filenames']
            caption = row['captions']
            # Preprocess the caption
            # cap_tokens = re.findall(r'\b[\w\']+\b', caption)
            cap_tokens = preprocess_text(caption, stopwords)
            if file in text_dict:
                text_dict[file].append(cap_tokens)
            else:
                text_dict[file] = [cap_tokens]
    return text_dict


def read_queries_from_file(filename):
    """
    Reads all the queries from a file and returns them as a list.
    """
    queries = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            query = line.strip().split(' ', 1)[1]
            queries.append(query)
  
    return queries

def write_results_to_file(results, filename):
    """
    Writes the results to a file given the dict with keys as query numbers and values as doc_ids.
    """
    with open(filename, 'w') as f:
        for query_num, doc_ids in results.items():
            for doc_id in doc_ids:
                f.write(f"{query_num},{doc_id}\n")
                
                
def write_ranked_results_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding here
        for query_num, doc_data in results.items():
            for doc_id, score in doc_data:
                f.write(f"{query_num},{doc_id},{round(score, 4)}\n")


