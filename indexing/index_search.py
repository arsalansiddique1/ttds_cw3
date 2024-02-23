import re
import string
import csv
import time
from itertools import filterfalse
from collections import defaultdict

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

file_path = 'images_with_captions.csv'
captions_by_title = read_csv_file(file_path)


'''
# Print the text data dictionary
for title, captions in captions_by_title.items():
    print(f"Title: {title}")
    print("Captions:")
    for caption in captions:
        print(f"-{caption}")
'''

# Index creation
def create_positional_inverted_index(text_dict):
    inverted_index = {}
    for title, captions in text_dict.items():
        for caption_index, caption_tokens in enumerate(captions):
            for position, token in enumerate(caption_tokens):
                if token in inverted_index:
                    if title in inverted_index[token]:
                        inverted_index[token][title].append((caption_index, position))
                    else:
                        inverted_index[token][title] = [(caption_index, position)]
                else:
                    inverted_index[token] = {title: [(caption_index, position)]}
    return inverted_index

# Create positional inverted index
positional_index = create_positional_inverted_index(captions_by_title)

def save_index_to_file(positional_index, file_path):
    with open(file_path, 'w', encoding='utf-8') as index_file:
        for term, postings in positional_index.items():
            # Calculate term frequency
            term_frequency = sum(len(positions) for positions in postings.values())
            index_file.write(f'Term: {term}\n')
            index_file.write(f'Frequency: {term_frequency}\n')
            for doc_id, positions in postings.items():
                index_file.write(f'Document: {doc_id}\n')
                for position in positions:
                    index_file.write(f'Position: {position}\n')
            index_file.write('\n')

# Save the positional inverted index to a file
save_index_to_file(positional_index, 'index.txt')


# Load index
def load_index_from_file(file_path):
    positional_index = {}
    with open(file_path, 'r', encoding='utf-8') as index_file:
        current_term = None
        current_postings = {}
        for line in index_file:
            line = line.strip()
            if line.startswith('Term:'):
                # Start of a new term
                if current_term is not None:
                    positional_index[current_term] = current_postings
                current_term = line.split(': ')[1].strip()
                current_postings = {}
            elif line.startswith('Document:'):
                # Start of document entry
                doc_id = line.split(': ')[1].strip()
                current_positions = []
            elif line.startswith('Position:'):
                # Position entry
                position = tuple(map(int, line.split(': ')[1].strip()[1:-1].split(', ')))
                current_positions.append(position)
            elif line == '':
                # End of term entry
                current_postings[doc_id] = current_positions
        # Add the last term
        if current_term is not None:
            positional_index[current_term] = current_postings
    return positional_index

# Load the positional inverted index from the file
positional_index = load_index_from_file('index.txt')

# Boolean search
def boolean_search(query, positional_index):
    # Split the query into terms
    terms = query.split()
    result = None
    for term in terms:
        if term in positional_index:
            # Initialize result with the postings list of the first term
            if result is None:
                result = set(positional_index[term].keys())
            # Perform intersection with postings lists of subsequent terms
            else:
                result &= set(positional_index[term].keys())
    return result if result else set()

# Proximity search
def proximity_search(query, k, positional_index):
    # Split the query into terms
    terms = query.split()
    result = None
    for term in terms:
        if term in positional_index:
            # Initialize result with the postings list of the first term
            if result is None:
                result = set(positional_index[term].keys())
            # Perform intersection with postings lists of subsequent terms
            else:
                result &= set(positional_index[term].keys())
    # Filter results based on proximity
    if result:
        proximity_results = set()
        for doc_id in result:
            positions_lists = [positional_index[term][doc_id] for term in terms if doc_id in positional_index[term]]
            for positions in zip(*positions_lists):
                if max(positions) - min(positions) <= k:
                    proximity_results.add(doc_id)
                    break
        return proximity_results
    else:
        return set()

# Phrase search
def phrase_search(query, positional_index):
    # Split the query into terms
    terms = query.split()
    result = None
    for term in terms:
        if term in positional_index:
            # Initialize result with the postings list of the first term
            if result is None:
                result = set(positional_index[term].keys())
            # Perform intersection with postings lists of subsequent terms
            else:
                result &= set(positional_index[term].keys())
    # Filter results based on phrase match
    if result:
        phrase_results = set()
        for doc_id in result:
            positions_lists = [positional_index[term][doc_id] for term in terms if doc_id in positional_index[term]]
            for positions in zip(*positions_lists):
                if all(positions[i] == positions[i-1] + 1 for i in range(1, len(positions))):
                    phrase_results.add(doc_id)
                    break
        return phrase_results
    else:
        return set()
    
    # Boolean search with timing
def boolean_search_with_timing(query, positional_index):
    start_time = time.perf_counter()  # Start timing
    # Original boolean search code
    result = boolean_search(query, positional_index)
    end_time = time.perf_counter()  # End timing
    duration = end_time - start_time  # Calculate duration
    print(f"Boolean Search Time: {duration:.6f} seconds")
    return result

# Proximity search with timing
def proximity_search_with_timing(query, k, positional_index):
    start_time = time.perf_counter()  # Start timing
    # Original proximity search code
    result = proximity_search(query, k, positional_index)
    end_time = time.perf_counter()  # End timing
    duration = end_time - start_time  # Calculate duration
    print(f"Proximity Search Time: {duration:.6f} seconds")
    return result

# Phrase search with timing
def phrase_search_with_timing(query, positional_index):
    start_time = time.perf_counter()  # Start timing
    # Original phrase search code
    result = phrase_search(query, positional_index)
    end_time = time.perf_counter()  # End timing
    duration = end_time - start_time  # Calculate duration
    print(f"Phrase Search Time: {duration:.6f} seconds")
    return result




# Testing queries
boolean_result = boolean_search_with_timing('birmingham AND birmingham', positional_index)
print("Boolean Search Result:", boolean_result)

proximity_result = proximity_search_with_timing('german' 'derffling', 10, positional_index)
print("Proximity Search Result:", proximity_result)

phrase_result = phrase_search_with_timing('main airport', positional_index)
print("Phrase Search Result:", phrase_result)



# queries processing? results ranking?

