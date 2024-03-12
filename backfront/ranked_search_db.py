import json
import os
import psycopg2
import re
from nltk.stem import PorterStemmer
import pandas as pd
import sys
import numpy as np
from utils import *
import connect_connector
import sqlalchemy

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then


def get_matching_rows(terms):
    with conn.cursor() as cursor:
        str_terms = "'" + "', '".join(terms) + "'"
        sql =f"""
        SELECT * FROM terms_json WHERE term = ANY(%s);
        """
        # Bind the term parameter to the statement
        cursor.execute(sql, (terms,))

        matching_rows = cursor.fetchall()

        return matching_rows

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

def retrieve_image_data(ids):
    with conn.cursor() as cursor:
        ids_str = ', '.join(ids)

        sql = f"SELECT DISTINCT ON (title, caption) * FROM captions2 WHERE id IN %s;"

        # Execute the query with the list of IDs as a parameter
        cursor.execute(sql, (tuple(ids),))

        # Fetch all rows
        output_dict = dict()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        output_dict = {row[0]: dict(zip(columns, row)) for row in cursor.fetchall()}

        return output_dict

    
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