from utils import *
from tfidf_and_bm25_scoring import *
from collections import defaultdict, Counter

def process_top_documents(top_docs, captions_by_file, n_t):
    """
    Helper: Append the content of all the n_d documents together
    """
    all_captions = []
    for filename, tfidf_scor in top_docs:
        if filename in captions_by_file:
            captions = captions_by_file[filename]
            all_captions.append(captions)
    """
    For every term in the appended captions, calculate the TF-IDF score, using the formula tf.log(N/df)
    """
    # Step 1: Calculate term frequencies (TF) within the captions
    term_frequencies = Counter()
    for captions in all_captions:
        for terms in captions:
            term_frequencies.update(terms)  # Update term frequencies
    
    # Step 2: Calculate TF-IDF scores for each term
    tfidf_scores = {}
    total_docs = len(all_captions)
    for term, tf in term_frequencies.items():
        df = sum(1 for captions in all_captions for cap in captions if term in cap)  # Document frequency
        idf = math.log(total_docs / df) if df != 0 else 0  # Inverse document frequency (avoid division by zero)
        tfidf_scores[term] = tf * idf  # TF-IDF score
        
    
    # Step 3: Sort terms by TF-IDF score
    sorted_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Step 4: Return the top n_t terms if specified
    if n_t is not None:
        sorted_terms = sorted_terms[:n_t]
    
    return dict(sorted_terms)


def run_pseudo_relevance_feedback(captions_by_file, inverted_index, n_d, n_t, queries_filename='queries.txt', results_filename='results_pseudo.txt'):
    queries = read_queries_from_file(queries_filename)
    results = {}

    for idx, query in enumerate(queries, 1): # start at 1
        # Retrieve top-ranked documents using original query
        top_docs = rank_docs(query, inverted_index, len(inverted_index['_doc_lengths']))[:n_d]  # top n_d ranked documents
        # Append the content of all the n_d documents together
        # For every term in the appeneded documents, calcualte the tfidf score. Use the formula tf.log(N/df)
        # Sort the terms by tfidf score. Report the top n_t terms
        results[idx] = process_top_documents(top_docs, captions_by_file, n_t)

    return print(results)
    #write_ranked_results_to_file(results, results_filename)

