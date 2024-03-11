from utils import *
import math
#from index_operations import load_index_from_file
from collections import defaultdict, Counter

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


def compute_idf(df, N):
    '''
    Compute IDF using the formula in slide 16 of lecture 7, with direct df input.
    Parameters:
    - df: The document frequency of the term (number of documents containing the term).
    - N: The total number of documents in the collection.
    '''
    if df == 0:
        return 0  # Prevent division by zero and log of zero issues
    return math.log10(N / df)



def compute_w_td(tf, idf):
    ''' 
    Calculate w_t.d as defined in slide 17 of lecture 7 (the RHS is idf)
    '''
    if tf == 0:
        return 0
    return (1 + math.log10(tf)) * idf

def rank_docs(query, inverted_index, N):
    scores = {docno: 0 for docno in inverted_index['_doc_lengths']}
    for term in query.split():
        if term in inverted_index:
            df = inverted_index[term]['df']  # Correctly extract 'df' as an integer
            idf = compute_idf(df, N)  # Pass 'df' correctly as an integer
            for docno, positions in inverted_index[term]['postings'].items():
                tf = len(positions)
                w_td = compute_w_td(tf, idf)
                scores[docno] += w_td
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)




def produce_tfidf_results(inverted_index, queries_filename='queries.txt', results_filename='results.test.txt'):
    '''
    Given the query, the index, and the name of the resulting file, performs the TFIDF 
    ranking search, and writes the results to a new file with the specified name.
    '''
    queries = read_queries_from_file(queries_filename)  # Assuming this function reads queries correctly
    results = {}
    N = len(inverted_index['_doc_lengths'])  # Total number of documents

    for idx, query in enumerate(queries, 1):  # Start enumeration from 1 to match query IDs
        
        # Assuming you have a preprocessing function similar to what was commented out
        # preprocessed_query = preprocess_query(query)  # Implement this as needed

        ranked_docs = rank_docs(query, inverted_index, N)
        # Store only the top 150 ranked docs with a score > 0, as required
        results[idx] = [doc for doc in ranked_docs if doc[1] > 0][:150][:150]  # Filter docs with score = 0, only store top 150 as required
    write_ranked_results_to_file(results, results_filename)  # Assuming this function correctly writes the results
    
    ##### BM25 scoring
    
def compute_bm25(idf, tf, doc_len, avgdl, k1=1.5, b=0.75):
    """
    Compute the BM25 score for a single term in a document.
    """
    term_score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl))))
    return term_score

def bm25_rank_docs(query, inverted_index, k1=1.5, b=0.75):
    avgdl = sum(inverted_index['_doc_lengths'].values()) / len(inverted_index['_doc_lengths'])
    total_docs = len(inverted_index['_doc_lengths'])
    scores = defaultdict(float)

    for term in query.split():
        if term in inverted_index:  # Ensure term exists
            df = inverted_index[term]['df']  # Document frequency
            idf = compute_idf(df, total_docs)  # Adjust compute_idf to accept df and total_docs
            for doc, positions in inverted_index[term]['postings'].items():
                tf = len(positions)  # Term frequency
                doc_len = inverted_index['_doc_lengths'][doc]
                score = compute_bm25(idf, tf, doc_len, avgdl, k1, b)
                scores[doc] += score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)



def produce_bm25_results(inverted_index, queries_filename='queries.txt', results_filename='results.bm25.txt'):
    """
    Given the query and the index, performs the BM25 ranking search and writes the results to a file.
    """
    queries = read_queries_from_file(queries_filename)

    results = {}
    
    for idx, query in enumerate(queries, 1):
        ranked_docs = bm25_rank_docs(query, inverted_index)
        results[idx] = ranked_docs[:150]  # Assuming the desire to keep the top 150 results
    
    write_ranked_results_to_file(results, results_filename)
    



