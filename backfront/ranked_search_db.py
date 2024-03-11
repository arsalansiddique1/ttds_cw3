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

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()

stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")
N = 8566975 #should be recalculated every now and then


def get_matching_rows(terms):
    with db.connect() as conn:
        sql =f"""
        SELECT term,
            json_object_agg(id, positions) AS id_positions
        FROM (
            SELECT term,
                id,
                ARRAY_AGG(position ORDER BY position) AS positions
            FROM middle
            WHERE term = ANY(:terms)
            GROUP BY term, id
        ) AS subquery
        GROUP BY term;
        """

        stmt = sqlalchemy.text(sql)
        # Bind the term parameter to the statement
        stmt = stmt.bindparams(terms=terms)
        result = conn.execute(stmt)

        matching_rows = result.fetchall()

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
    with db.connect() as conn:
        ids_str = ', '.join(ids)

        sql = f"SELECT DISTINCT ON (title, caption) * FROM captions2 WHERE id IN ({ids_str});"

        stmt = sqlalchemy.text(sql)
        result = conn.execute(stmt)

        # Get column names from the result set's description attribute
        columns = [desc[0] for desc in result.cursor.description]

        # Fetch all rows
        matching_rows = result.fetchall()
        output_dict = {row[0]: dict(zip(columns, row)) for row in matching_rows}

        return output_dict
    
# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python script.py 'query'")
#         sys.exit(1)

#     query = sys.argv[1]
#     tfidfs = ranked_tfidf_search(query)
#     sorted_results = sorted(tfidfs, key=tfidfs.get, reverse=True)[:500]
#     image_data = retrieve_image_data(sorted_results)
#     captions = [image_data[int(i)]["caption"] for i in sorted_results if int(i) in image_data]
#     print(captions)

# if __name__ == "__main__":
#     main()