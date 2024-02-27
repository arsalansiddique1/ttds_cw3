import re
import string
import csv
import time
import json
from itertools import filterfalse
from collections import defaultdict
from nltk.stem import PorterStemmer
from memory_profiler import profile


#@profile #Meauring memory consumption for creating indices
# Index creation (image/file)
def create_positional_inverted_index(text_dict):
    inverted_index = {}
    for file, captions in text_dict.items():
        for caption_index, caption_tokens in enumerate(captions):
            for position, token in enumerate(caption_tokens):
                if token in inverted_index:
                    if file in inverted_index[token]:
                        inverted_index[token][file].append((caption_index, position))
                    else:
                        inverted_index[token][file] = [(caption_index, position)]
                else:
                    inverted_index[token] = {file: [(caption_index, position)]}
    return inverted_index

def save_index_to_json(positional_index, file_path):
    with open(file_path, 'w', encoding='utf-8') as index_file:
        json.dump(positional_index, index_file, ensure_ascii=False, indent=4)

'''
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
'''  

            #load index
def load_index_from_file(file_path):
    positional_index = {}
    with open(file_path, 'r', encoding='utf-8') as index_file:
        current_term = None
        current_postings = {}
        doc_id = None  # Keep track of the current document ID
        for line in index_file:
            line = line.strip()
            if line.startswith('Term:'):
                # If not the first term, save the previous term's postings
                if current_term is not None:
                    positional_index[current_term] = current_postings
                current_term = line.split(': ')[1]
                current_postings = {}
            elif line.startswith('Document:'):
                # If not the first document under the current term, save positions for the previous document
                if doc_id is not None:
                    # No additional action needed here if positions are directly added to current_postings in the 'Position:' block
                    pass
                doc_id = line.split(': ')[1].strip()
                current_postings[doc_id] = []  # Prepare to collect positions for this document
            elif line.startswith('Position:'):
                position = tuple(map(int, line.split(': ')[1].strip()[1:-1].split(', ')))
                if doc_id in current_postings:  # Safety check, though doc_id should always be in current_postings at this point
                    current_postings[doc_id].append(position)
        
        # After finishing the file, save the last term's postings
        if current_term is not None:
            positional_index[current_term] = current_postings

    return positional_index
