import json
import os
import re
from nltk.stem import PorterStemmer
import pandas as pd
from utils import preprocess_text, extract_stopwords


with open('index.json') as f:
   pos_inverted_index = json.load(f)

doc_ids = pd.read_csv("images_with_captions.csv").filenames.values

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

# STOP_STEM = True
# #FILENAME = "../cw1collection/trec.5000.xml"
# FILENAME = "./trec.sample.xml"
# STOPWORDS_FILENAME = "./ttds_2023_english_stop_words.txt"

# # Load stopwords
# with open(file=STOPWORDS_FILENAME, mode="r") as stopwords_file:
#     stopwords = set(stopwords_file.read().splitlines())


# #tokenise text
# def tokeniser(text):
#     text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
#     return text.split()

# #preprocess text by case folding and 
# def preprocess(text, stem_stop):
#     tokens = tokeniser(text)
#     if stem_stop:
#         stemmer = PorterStemmer()
#         tokens = [
#             stemmer.stem(token) for token in tokens if token.lower() not in stopwords
#         ]
#     return tokens

no_hits_placeholder = dict({'postings':{}})
#treat query by splitting it into parts by identifying AND or OR
def query_handler(query):
    output = list()
    splitByOr = query.split(" OR ")
    for p in splitByOr:
        splitByAnd = p.split(" AND ")
        output.append(splitByAnd)
    return output

#given locations of two terms identify where they appear closer to each other that dist 
def proximity_2_terms(term1_locs, term2_locs, dist):
    results = []
    for key in term1_locs:   
            term1_doc = key
            term1_pos = term1_locs[key]

            for key2 in term2_locs:
                    term2_doc = key2
                    term2_pos = term2_locs[key2]

                    if term1_doc == term2_doc:
                        for p in term1_pos:
                            for p2 in term2_pos:
                                if abs(p-p2) <= dist:
                                    results.append(key)
    return results

#phrase search by using proximity_2_terms with distance 1
def phrasesearch(query):
    terms = preprocess_text(query, stopwords)

    output = set()
    for i in range(len(terms)-1):
        term1_locs = pos_inverted_index.get(terms[i], no_hits_placeholder)['postings']
        term2_locs = pos_inverted_index.get(terms[i+1], no_hits_placeholder)['postings']

        results_two_terms = set(proximity_2_terms(term1_locs, term2_locs, 1))

        if i == 0: output = output.union(results_two_terms)
        else: output = output.intersection(results_two_terms)
    
    return output

#get the documents for the different search cases after splitting for AND or OR or operators
def getDocs(searchTerm):
    all_docs = set(doc_ids)
    if searchTerm[0] == '#':    #if hashtag then proximity search
        proximity_args = re.findall(r"[\w']+", searchTerm)

        processed_term1 = preprocess_text(proximity_args[1], stopwords).pop()
        processed_term2 = preprocess_text(proximity_args[2], stopwords).pop()

        term1_locs = pos_inverted_index.get(processed_term1, no_hits_placeholder)['postings']
        term2_locs = pos_inverted_index.get(processed_term2, no_hits_placeholder)['postings']

        searchResult = set(proximity_2_terms(term1_locs, term2_locs, int(proximity_args[0])))
        return searchResult
    elif searchTerm[0] == '"':  #if quotation marks phrase seach
        searchResult = phrasesearch(searchTerm)
        return searchResult
    elif "NOT " in searchTerm:  #if NOT get complement
        searchTerm = searchTerm[4:]
        searchTerm = preprocess_text(searchTerm, stopwords).pop() #add preprocess stop and stem
        searchResult = set(pos_inverted_index.get(searchTerm, no_hits_placeholder)['postings'].keys())
        return all_docs.difference(searchResult)
    else:                       #otherwise just get the docs associated with term
        searchTerm = preprocess_text(searchTerm, stopwords).pop() #preprocess search term
        searchResult = set(pos_inverted_index.get(searchTerm, no_hits_placeholder)['postings'].keys())
        return searchResult

#boolean search, standard search performed. deals with allqueries even if no AND or OR are identified
def bool_search(query):
    formatted_query = query_handler(query)

    docs = set() 
    for ors in formatted_query:
        andDocs = getDocs(ors[0])
        for ands in ors[1:]:    #before just ors, double check
            retrieved_docs = getDocs(ands)
            andDocs = andDocs.intersection(retrieved_docs)
        docs = docs.union(andDocs)
    return docs