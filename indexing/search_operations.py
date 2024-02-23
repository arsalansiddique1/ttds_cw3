import re
import string
import csv
import time
from itertools import filterfalse
from collections import defaultdict
from nltk.stem import PorterStemmer
#### Boolean search

def perform_search(query, inverted_index):
    '''
    Main function to perform boolean search. Identifies which type of boolean 
    query it is and calls the appropriate function
    '''
    if "#" in query:
        proximity_value = int(query.split('#')[1].split('(')[0]) #Remember it is of the form #dist(term1, term2)
        terms = query.split('(')[1].split(')')[0] # We only want what is between the parentheses
        
        return proximity_search(terms, proximity_value, inverted_index)
        
    elif "AND" in query:
        return and_search(query, inverted_index)
    
    elif "OR" in query:
        return or_search(query, inverted_index)
    
    elif query.startswith('"') and query.endswith('"'): # Then it is a phrase query that does not involve AND or OR
        return phrase_search(query, inverted_index)
    
    else:
        return simple_search(query, inverted_index)
        #return simple_search(query, inverted_index, stopwords)


#Helper functions all below

def preprocess_query_term(term, stopwords):
    
    #Helper function to preprocess a query term using the same steps as for the index creation
    
    tokens = re.findall(r'\b[\w\']+\b', term.lower())
    
    tokens = list(filterfalse(stopwords.__contains__, tokens))
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    
    return stemmed_tokens


def proximity_search(query, dist, inverted_index):
#def proximity_search(query, dist, inverted_index, stopword):
    '''
    Performs a proximity search over the inverted index. Finds documents where the 
    distance between term1 and term2 is less than or equal to dist (after stop words removal).
    '''
    
    terms = query.strip().split(',')
    term1 = terms[0].strip()
    term2 = terms[1].strip()
    #term1 = preprocess_query_term(terms[0], stopwords)[0]
    #term2 = preprocess_query_term(terms[1], stopwords)[0]
    term1_positions = inverted_index.get(term1, {})
    term2_positions = inverted_index.get(term2, {})
    # Assuming doc_id is the document identifier, and positions are lists of (caption_index, word_position) tuples
    result_docs = []
    for doc_id in term1_positions:
        if doc_id in term2_positions:
            for pos1 in term1_positions[doc_id]:
                for pos2 in term2_positions[doc_id]:
                    # Check if the terms are in the same caption before comparing positions
                    if pos1[0] == pos2[0]:  # pos1[0] and pos2[0] are caption_indices
                        # Now compare the word positions within the same caption
                        if abs(pos1[1] - pos2[1]) <= dist:  # pos1[1] and pos2[1] are word_positions
                            result_docs.append(doc_id)
                            break  # Found a valid pair, no need to check more positions for pos2
                if doc_id in result_docs:
                    break  # Found a valid pair, no need to check more positions for pos1

    return result_docs
def and_search(query, inverted_index):
    '''
    Performs an AND search over the inverted index
    '''
    if "AND NOT" in query:
        terms = query.split(' AND NOT ')
    else: 
        terms = query.split(' AND ')
       
    # We do these if else statements to check if one of the terms is a phrase
    if terms[0].startswith('"') and terms[0].endswith('"'):
        # This would give us the set of documents which would contain the first phrase search
        #term1_docs = phrase_search(terms[0], inverted_index, stopwords)
        term1_docs = phrase_search(terms[0], inverted_index)

    else:
        term1 = terms[0]
        #term1 = preprocess_query_term(terms[0], stopwords)[0]
        term1_docs = inverted_index.get(term1, {}).keys()
        term1_docs = [doc for doc in term1_docs]


    if terms[1].startswith('"') and terms[1].endswith('"'):
        #term2_docs = phrase_search(terms[1], inverted_index, stopwords)
        term2_docs = phrase_search(terms[1], inverted_index)
    else:
        term2 = terms[1]
        term2_docs = inverted_index.get(term2, {}).keys()
        term2_docs = [doc for doc in term2_docs]
    
    if "AND NOT" in query:
        return sorted([doc for doc in term1_docs if doc not in term2_docs])
    else:
        return sorted([doc for doc in term1_docs if doc in term2_docs])


def or_search(query, inverted_index):
#def or_search(query, inverted_index, stopwords):
    '''
    Performs an OR search over the inverted index
    '''
    if "OR NOT" in query:
        terms = query.split(' OR NOT ')
    else: 
        terms = query.split(' OR ')
        
    # Checking if the term is a phrase search
    if terms[0].startswith('"') and terms[0].endswith('"'):
        term1_docs = phrase_search(terms[0], inverted_index)
        #term1_docs = phrase_search(terms[0], inverted_index, stopwords)
    else:
        term1 = terms[0]
        #term1 = preprocess_query_term(terms[0], stopwords)[0]
        term1_docs = inverted_index.get(term1, {}).keys()
        term1_docs = [doc for doc in term1_docs]
   

    if terms[1].startswith('"') and terms[1].endswith('"'):
        term2_docs = phrase_search(terms[1], inverted_index)
        #term2_docs = phrase_search(terms[1], inverted_index, stopwords)
    else:
        term2 = terms[1]
        #term2 = preprocess_query_term(terms[1], stopwords)[0]
        term2_docs = inverted_index.get(term2, {}).keys()
        term2_docs = [doc for doc in term2_docs]

    
    all_docs = []
    for posting in inverted_index.values():
        all_docs.extend(posting.keys())

    if "OR NOT" in query: 
        # I think this will probably will not be used since unless term2 is very common, it will return almost all docs
        or_not_result = list(set(term1_docs) | (set(all_docs) - set(term2_docs)))
        return sorted([or_not_result]) 

    else:
        or_result = list(set(term1_docs) | set(term2_docs))
        return sorted([or_result])  # Assuming or_result is a list or set of document IDs as strings

    
def phrase_search(query, inverted_index):
    '''
    Performs a phrase search over the inverted index, assuming there are 2 terms,
    and positions are stored as tuples in the format (caption_index, word_position).
    '''
    terms = query.replace('"', '').split()  # Assuming query is a phrase wrapped in quotes
    term1, term2 = terms[0], terms[1]

    term1_docs_positions = inverted_index.get(term1, {})
    term2_docs_positions = inverted_index.get(term2, {})

    result_docs = []

    for doc in term1_docs_positions:
        if doc in term2_docs_positions:
            # Iterate through positions of term1 in the document
            for pos1 in term1_docs_positions[doc]:
                # Check if there's a directly following position in term2's positions
                following_pos = (pos1[0], pos1[1] + 1)  # Increment word position
                if following_pos in term2_docs_positions[doc]:
                    result_docs.append(doc)
                    break  # Found a match, move to the next document

    return sorted(result_docs)


def simple_search(query, inverted_index):
#def simple_search(query, inverted_index, stopwords):
    '''
    Performs a simple search over the inverted index
    '''
    docs = inverted_index.get(query, {}).keys()
    #preprocessed_query = preprocess_query_term(query, stopwords)[0]
    return sorted([doc for doc in docs])

## All of the functions above were helper functions of perform_search.