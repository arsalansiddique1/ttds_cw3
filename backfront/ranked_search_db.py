import sys
import numpy as np
from utils import *
from db_retrieval_functions import get_matching_rows, retrieve_image_data

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then

#implement ranked search
def ranked_tfidf_search(query):
    query = preprocess_text(query, stopwords)
    #N = len(doc_ids)
    tfidfs = {} # Dictionary to store {docnumber: tfidf score}

    #tfidf implemented like in lectures
    def tfidf(tf, df):
        return (1 + np.log10(tf)) * (np.log10(N/df))

    term_freqs = get_matching_rows(query)
    for term in term_freqs:
        positions = term[1]
        docfreq = len(positions)
        for doc in positions:
                vals = positions[doc]
                termfreq = len(vals)
                t = tfidf(termfreq, docfreq)

                if doc not in tfidfs.keys():
                    tfidfs[doc] = t
                else:
                    newval = tfidfs[doc].__add__(t)
                    tfidfs[doc] = newval
    return tfidfs


MAX_NUM_RESULTS = 500
def ranked_search(query):
    tfidfs = ranked_tfidf_search(query)
    sorted_results = sorted(tfidfs, key=tfidfs.get, reverse=True)[:MAX_NUM_RESULTS]
    image_data = retrieve_image_data(sorted_results)
    results = [image_data[int(i)] for i in sorted_results if int(i) in image_data]
    return results
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py 'query'")
        sys.exit(1)

    query = sys.argv[1]
    tfidfs = ranked_tfidf_search(query)
    sorted_results = sorted(tfidfs, key=tfidfs.get, reverse=True)[:500]
    print(sorted_results)
    image_data = retrieve_image_data(sorted_results)
    captions = [image_data[int(i)]["caption"] for i in sorted_results if int(i) in image_data]

if __name__ == "__main__":
    main()