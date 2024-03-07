import psycopg2
import os
from utils import preprocess_text, extract_stopwords

# Connect to PostgreSQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
    with conn.cursor() as cursor:
        with conn.cursor() as cur2:
            with conn.cursor() as cur3:
                with conn.cursor() as cur4:
                    # Load stopwords
                    stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

                    # Iterate through caption table
                    cursor.execute("SELECT id, caption FROM captions2_copy")
                    for document_id, caption in cursor.fetchall():
                        # Process the row
                        terms_encountered = set()
                        cap_tokens = preprocess_text(caption, stopwords)
                        document_length = len(cap_tokens)

                        print(document_id)
                        print(cap_tokens)
                        break

                        # # Update document length in caption table
                        # cur2.execute("UPDATE captions2_copy SET doc_length = %s WHERE id = %s", (document_length, document_id))

                        # # Update terms table and middle table
                        # for pos, term in enumerate(cap_tokens):
                        #     # Update document frequency in terms table
                        #     if term not in terms_encountered:
                        #         cur3.execute("INSERT INTO terms (term, doc_frequency) VALUES (%s, 1) ON CONFLICT (term) DO UPDATE SET doc_frequency = terms.doc_frequency + 1", (term,))
                        #         terms_encountered.add(term)

                        #     # Insert into middle table
                        #     cur4.execute("INSERT INTO middle (id, term, position) VALUES (%s, %s, %s)", (document_id, term, pos))

                        # Commit every 1000 rows
                        if document_id % 1000 == 0:
                            conn.commit()
                            print(document_id)
