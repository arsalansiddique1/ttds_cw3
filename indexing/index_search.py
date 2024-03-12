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
from tfidf_and_bm25_scoring import *
from utils import *
from prf import *

####### Main method for loading indexes and perfomring searches #######

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

file_path = '../caption_extraction/try.csv' 
captions_by_file = read_csv_file(file_path, stopwords)


# Create positional inverted index and measure execution time
start_time = time.perf_counter()  # Start timing
positional_index = create_positional_inverted_index(captions_by_file)
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Index creation Time: {duration:.6f} seconds")
# Save the positional inverted index to a file
#save_index_to_file(positional_index, 'index.txt')

save_index_to_json(positional_index, 'index.json')

# Load the positional inverted index from the file
#positional_index = load_index_from_file('index.txt')
# Load from json file
json_data = read_json_file('index.json')

positional_index = json_data



#Testing TF-IDF scoring (seems to work)
produce_tfidf_results(inverted_index = positional_index, queries_filename="queries.txt", results_filename="tfidf_results.txt")
#Testing BM25 Scoring
produce_bm25_results(inverted_index = positional_index, queries_filename='queries.txt', results_filename='results.bm25.txt')


# Query Expansion using pseudo_relevance_feedback from lecture 11 & lab 5
run_pseudo_relevance_feedback(captions_by_file, positional_index, n_d=15, n_t=3,queries_filename='queries.txt', results_filename='results_pseudo.txt')


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
