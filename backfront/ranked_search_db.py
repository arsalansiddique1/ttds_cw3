import json
import os
import psycopg2
import re
from nltk.stem import PorterStemmer
import pandas as pd
import sys
import numpy as np
from utils import *

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then

# Connect to PostgreSQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

print("yyyy")


def get_matching_rows(terms):
    print(DB_NAME)
    print(DB_USER)
    print(DB_PASSWORD)
    print(DB_HOST)
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    print(conn)
    cursor = conn.cursor()
    print("connected")
    sql = """ 
    SELECT term,
        json_object_agg(id, positions) AS id_positions
    FROM (
        SELECT term,
            id,
            ARRAY_AGG(position ORDER BY position) AS positions
        FROM middle
        WHERE term = ANY(%s)
        GROUP BY term, id
    ) AS subquery
    GROUP BY term;
    """

    # Execute the query with the list of terms as a parameter
    cursor.execute(sql, (terms,))
    print("execution failed")

    # Fetch all rows
    matching_rows = cursor.fetchall()

    # Close connection
    conn.close()

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
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = conn.cursor()

    sql = f"SELECT DISTINCT ON (title, caption) * FROM captions2 WHERE id IN %s;"

    # Execute the query with the list of IDs as a parameter
    cursor.execute(sql, (tuple(ids),))

    # Fetch all rows
    output_dict = dict()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    output_dict = {row[0]: dict(zip(columns, row)) for row in cursor.fetchall()}

    # Close connection
    conn.close()

    return output_dict