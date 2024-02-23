import math
import re
import string
import csv
import time
from itertools import filterfalse
from collections import defaultdict
from nltk.stem import PorterStemmer
from search_operations import *
from index_operations import *
from tfidf_scoring import *
stopwords_file = "ttds_2023_english_stop_words.txt"

# Reading the csv file
def read_csv_file(file_path):
    text_dict = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            title = row['title']
            caption = row['captions']
            # Tokenize the caption
            cap_tokens = re.findall(r'\b[\w\']+\b', caption)
            if title in text_dict:
                text_dict[title].append(cap_tokens)
            else:
                text_dict[title] = [cap_tokens]
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



file_path = 'images_with_captions.csv'
captions_by_title = read_csv_file(file_path)


# Create positional inverted index
positional_index = create_positional_inverted_index(captions_by_title)

# Save the positional inverted index to a file
save_index_to_file(positional_index, 'index.txt')


# Load the positional inverted index from the file
positional_index = load_index_from_file('index.txt')




#Testing TF-IDF scoring (seems to work)
produce_tfidf_results(inverted_index = positional_index, queries_filename="queries.txt", results_filename="results.test.txt")

'''
# Testing queries
start_time = time.perf_counter()  # Start timing
simple_result = perform_search('wilhelm', positional_index)
print("Simple Search Result:", simple_result)
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Simple Search Time: {duration:.6f} seconds")

start_time = time.perf_counter()  # Start timing
boolean_result = perform_search('allah AND NOT birka', positional_index)
print("Boolean Search Result:", boolean_result)
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Boolean Search Time: {duration:.6f} seconds")

start_time = time.perf_counter()  # Start timing
proximity_result = perform_search('#6(turbofan, pylon)', positional_index)
print("Proximity Search Result:", proximity_result)
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Proximity Search Time: {duration:.6f} seconds")


start_time = time.perf_counter()  # Start timing
phrase_result = perform_search('"black diamond"', positional_index)
print("Phrase Search Result:", phrase_result)
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Prase Search Time: {duration:.6f} seconds")


'''
