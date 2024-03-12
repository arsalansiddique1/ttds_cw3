import json
import os
import re
import numpy as np
from nltk.stem import PorterStemmer
import pandas as pd
import sys
from utils import preprocess_text, extract_stopwords
from db_retrieval_functions import retrieve_image_data, fetch_db_single_term

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then

#treat query by splitting it into parts by identifying AND or OR
def query_handler(query):
    output = list()
    splitByOr = query.split(" OR ")
    for p in splitByOr:
        splitByAnd = p.split(" AND ")
        output.append(splitByAnd)
    return output

#given locations of two terms identify where they appear closer to each other that dist 
def proximity_2_terms(term1_locs, term2_locs, dist, phrase=False):
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
                                if abs(p-p2) <= dist and not phrase:
                                    results.append(key)
                                elif p-p2 == -1 and phrase:
                                    results.append(key)
    return results

#phrase search by using proximity_2_terms with distance 1
def phrasesearch(query):
    terms = preprocess_text(query, stopwords)

    if(len(terms==1)): return getDocs(terms[0]) #phrase with only one word is term search

    output = set()
    for i in range(len(terms)-1):
        term1_locs = fetch_db_single_term[0](terms[i])[1]
        term2_locs = fetch_db_single_term[0](terms[i+1])[1]

        results_two_terms = set(proximity_2_terms(term1_locs, term2_locs, 1, phrase=True))

        if i == 0: output = output.union(results_two_terms)
        else: output = output.intersection(results_two_terms)
    
    return output

#get the documents for the different search cases after splitting for AND or OR or operators
def getDocs(searchTerm):
    print("x", searchTerm)
    searchTerm = searchTerm.strip()
    if searchTerm[0] == '~':    #if hashtag then proximity search
        print("prox search ", searchTerm)
        proximity_args = re.findall(r"[\w']+", searchTerm)

        processed_term1 = preprocess_text(proximity_args[1], stopwords).pop()
        processed_term2 = preprocess_text(proximity_args[2], stopwords).pop()

        term1_locs = fetch_db_single_term(processed_term1)[0][1]
        term2_locs = fetch_db_single_term(processed_term2)[0][1]

        searchResult = set(proximity_2_terms(term1_locs, term2_locs, int(proximity_args[0])))
        return searchResult
    elif searchTerm[0] == '"':  #if quotation marks phrase seach
        searchResult = phrasesearch(searchTerm)
        return searchResult
    elif "NOT " in searchTerm:  #if NOT get complement
        searchTerm = searchTerm[4:]
        searchTerm = preprocess_text(searchTerm, stopwords).pop() #add preprocess stop and stem
        searchResult = set(fetch_db_single_term(searchTerm)[0][1])
        return searchResult
    else:                       #otherwise just get the docs associated with term
        searchTerm = preprocess_text(searchTerm, stopwords).pop() #preprocess search term
        searchResult = set(fetch_db_single_term(searchTerm)[0][1])
        return searchResult

MAX_NUM_RESULTS = 500
#boolean search, standard search performed. deals with allqueries even if no AND or OR are identified
def bool_search_db(query):
    print(query)
    query = query.strip()
    formatted_query = query_handler(query)
    print(formatted_query)

    docs = set() 
    for ors in formatted_query:
        andDocs = getDocs(ors[0])
        for ands in ors[1:]:    #before just ors, double check
            retrieved_docs = getDocs(ands)
            if("NOT " in ands): 
                andDocs = andDocs.difference(retrieved_docs)
            else: andDocs = andDocs.intersection(retrieved_docs)
        docs = docs.union(andDocs)

    image_data = retrieve_image_data((list(docs)))
    results = list(image_data.values())[:MAX_NUM_RESULTS]
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py 'query'")
        sys.exit(1)

    query = sys.argv[1]
    ids = bool_search_db(query)
    
    image_data = retrieve_image_data(list(ids))
    captions = [i["caption"] for i in image_data.values()]
    for caption in captions:
        print(caption)

if __name__ == "__main__":
    main()