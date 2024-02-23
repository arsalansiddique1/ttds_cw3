from utils import *
import math
from index_operations import load_index_from_file

#### TFIDF scoring

def get_all_docnos(inverted_index):
    docnos_set = set()
    for _, postings in inverted_index.items():
        for docno in postings:
            docnos_set.add(docno) # Since it is a set so it does not have duplicates
    return sorted([i for i in docnos_set])


def compute_tf(term, docno, inverted_index):
    '''
    Compute tf(t,d): number of times term t appeared in document d
    '''
    if term in inverted_index and docno in inverted_index[term]:
        return len(inverted_index[term][docno])
    return 0


def compute_idf(term, inverted_index, N):
    '''
    Compute IDF using the formula in slide 16 of lecture 7
    '''
    # df(t): number of documents term t appeared in
    df = len(inverted_index.get(term, {}))
    if df == 0:
        return 0
    return math.log10(N / df)


def compute_w_td(tf, idf):
    ''' 
    Calculate w_t.d as defined in slide 17 of lecture 7 (the RHS is idf)
    '''
    if tf == 0:
        return 0
    return (1 + math.log10(tf)) * idf

def rank_docs(query, inverted_index):
    '''
    Rank documents for a given query using TFIDF as defined in slide 17 of lecture 7
    '''
    all_docnos = get_all_docnos(inverted_index)
    scores = {docno: 0 for docno in all_docnos}
    
    # In these loops we don't need to check when t \in q and d, since if it does not satisfy this and
    # condition, then compute_idf and/or compute_w_td will be 0, so we can safely sum over multiple 0s
    for term in query.split():
        idf = compute_idf(term, inverted_index, len(all_docnos))
        for docno, _ in inverted_index.get(term, {}).items():
            tf = compute_tf(term, docno, inverted_index)
            w_td = compute_w_td(tf, idf)
            scores[docno] += w_td
    
    # Sort by scores
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def produce_tfidf_results(inverted_index=load_index_from_file("index.txt"), queries_filename='queries.txt', results_filename = 'results.test.txt'):
    '''
    Given the query, the index, and the name of the resulting file, performs the TFIDF 
    ranking search, and writes the results to a new file with the specified name.
    '''
    queries = read_queries_from_file(queries_filename) # We can reuse this function
    results = {}

    for idx, query in enumerate(queries, 1):  # Start enumeration from 1 as in the queries file
        
        # Preprocess query since we don't do it in the rank_docs function
        #preprocessed_query_terms = preprocess_query_term(query, stopwords)
        # Since the above function returns a list of strings, we want to put them back again as a single string
        #preprocessed_query = " ".join(preprocessed_query_terms)
        ranked_docs = rank_docs(query, inverted_index)
        #ranked_docs = rank_docs(preprocessed_query, inverted_index)
        results[idx] = [doc for doc in ranked_docs if doc[1] > 0][:150][:150]  # Filter docs with score = 0, only store top 150 as required

    write_ranked_results_to_file(results, results_filename)


def write_ranked_results_to_file(results, filename):
    """
    Writes the TFIDF results to a file given the dict with keys as query numbers and values as doc_ids, scores.
    """
    with open(filename, 'w') as f:
        for query_num, doc_data in results.items():
            for doc_id, score in doc_data:
                f.write(f"{query_num},{doc_id},{round(score, 4)}\n") # Since it is specified that round to 4 dec places

