import json
import os
import psycopg2
import re
from nltk.stem import PorterStemmer
import pandas as pd
import sys
from search_module import *
from utils import *

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then
MAX_NUM_RESULTS = 500

# Retrieve environment variables
INSTANCE_CONNECTION_NAME='wikimage:europe-west1:generaldb2'
DB_PORT = '5432'
DB_NAME = 'wikimage'
DB_USER = 'postgres'
DB_PASSWORD = ')>K>x%v1r0X9aNj7'
DB_HOST = '35.240.34.228'

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()

def get_matching_rows(terms):
    # Create a cursor object

    # Construct the parameterized SQL query
    #sql = "SELECT term, id, ARRAY_AGG(position ORDER BY position) AS positions FROM middle WHERE term = ANY(%s) GROUP BY term, id;"
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
    
    # Fetch all rows
    matching_rows = cursor.fetchall()

    return matching_rows

#implement ranked search
def rankedir_search(query):
    query = preprocess_text(query, stopwords)
    N = len(doc_ids)
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

    sql = f"SELECT * FROM captions2 WHERE id IN %s;"
            
    # Execute the query with the list of IDs as a parameter
    cursor.execute(sql, (tuple(ids),))

    # Fetch all rows
    output_dict = dict()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    output_dict = {row[0]: dict(zip(columns[1:], row[1:])) for row in cursor.fetchall()}

    return output_dict

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py 'query'")
        sys.exit(1)

    query = sys.argv[1]
    tfidfs = rankedir_search(query)
    sorted_results = sorted(tfidfs, key=tfidfs.get, reverse=True)[:MAX_NUM_RESULTS]
    image_data = retrieve_image_data(sorted_results)
    captions = [image_data[int(i)]["caption"] for i in sorted_results]
    print(captions)

if __name__ == "__main__":
    main()