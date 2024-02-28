from utils import read_queries_from_file
from utils import *
import math
from index_operations import load_index_from_file
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
    
    ##### BM25 scoring
    
def compute_bm25(idf, tf, doc_len, avgdl, k1=1.5, b=0.75):
    """
    Compute the BM25 score for a single term in a document.
    """
    term_score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl))))
    return term_score

def bm25_rank_docs(query, inverted_index, k1=1.5, b=0.75):
    # Calculate document lengths and aggregate TF from the positional inverted index
    doc_lengths = calculate_document_lengths(inverted_index)
    aggregate_tf = calculate_aggregate_tf(inverted_index)
    avgdl = sum(doc_lengths.values()) / len(doc_lengths)
    
    total_docs = len(doc_lengths)
    scores = defaultdict(float)

    for term in query.split():
        idf = compute_idf(term, inverted_index, total_docs)  # Assuming IDF calculation adapts to non-positional data
        for doc, tf in aggregate_tf.get(term, {}).items():
            doc_len = doc_lengths[doc]
            score = compute_bm25(idf, tf, doc_len, avgdl, k1, b)
            scores[doc] += score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def produce_bm25_results(inverted_index, queries_filename='queries.txt', results_filename='results.bm25.txt'):
    """
    Given the query and the index, performs the BM25 ranking search and writes the results to a file.
    """
    queries = read_queries_from_file(queries_filename)
    print(queries)
    results = {}
    
    for idx, query in enumerate(queries, 1):
        ranked_docs = bm25_rank_docs(query, inverted_index)
        results[idx] = ranked_docs[:150]  # Assuming the desire to keep the top 150 results
    
    write_ranked_results_to_file(results, results_filename)
    
    
    


#2 util functions below which will be moved to relevant file once BM25 is working
def calculate_document_lengths(inverted_index):
    doc_lengths = defaultdict(int)
    for token, doc_positions in inverted_index.items():
        for doc, positions in doc_positions.items():
            doc_lengths[doc] += len(positions)  # Summing all positions (occurrences) of all tokens
    return doc_lengths

def calculate_aggregate_tf(inverted_index):
    aggregate_tf = defaultdict(lambda: defaultdict(int))
    for token, doc_positions in inverted_index.items():
        for doc, positions in doc_positions.items():
            aggregate_tf[token][doc] = len(positions)  # Total occurrences of token in doc
    return aggregate_tf


def write_ranked_results_to_file(results, filename):
    """
    Writes the TFIDF results to a file given the dict with keys as query numbers and values as doc_ids, scores.
    """
    with open(filename, 'w') as f:
        for query_num, doc_data in results.items():
            for doc_id, score in doc_data:
                f.write(f"{query_num},{doc_id},{round(score, 4)}\n") # Since it is specified that round to 4 dec places

