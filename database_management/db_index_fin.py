import psycopg2
import psycopg2.extras
import os
from utils import preprocess_text, extract_stopwords

# Connect to PostgreSQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

#define methods to decrease execution time - single string execution, and execute_batch
def string_insert_middle(cursor, values):
    argument_string = ",".join("('%s', '%s', '%s')" % (x, y, z) for (x, y, z) in values)
    cursor.execute("INSERT INTO middle (id, term, position) VALUES" + argument_string)

def execute_batch_insert_terms(cursor, values):
    psycopg2.extras.execute_batch(cursor, "INSERT INTO terms (term, doc_frequency) VALUES (%s, 1) ON CONFLICT (term) DO UPDATE SET doc_frequency = terms.doc_frequency + 1", values)

def execute_batch_update_captions(cursor, values):
    psycopg2.extras.execute_batch(cursor, "UPDATE captions2_copy SET doc_length = %s WHERE id = %s", values)

with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
    with conn.cursor() as cursor:
        # Load stopwords
        stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

        # Fetch data from the caption table
        cursor.execute("SELECT id, caption FROM captions2_copy ORDER BY id")

        while True:
            rows = cursor.fetchmany(1000)  # Fetch 1000 rows at a time
            if not rows:
                break
            
            #build data structure - lists of tuples
            data_to_insert_middle = []
            data_to_insert_terms = []
            data_to_update_caption = []
            for document_id, caption in rows:
                # Process the row
                terms_encountered = set()
                cap_tokens = preprocess_text(caption, stopwords)
                document_length = len(cap_tokens)

                # Update document length in data to update the caption table
                data_to_update_caption.append((document_length, document_id))
                    
                # Prepare data for batch insert into middle and terms table
                for pos, term in enumerate(cap_tokens):
                    data_to_insert_middle.append((document_id, term, pos))

                    if term not in terms_encountered:
                        data_to_insert_terms.append((term,))
                        terms_encountered.add(term)

            # Batch insert into terms table
            execute_batch_insert_terms(cursor, data_to_insert_terms)

            # Batch insert into middle table
            string_insert_middle(cursor, data_to_insert_middle)

            # Update caption table with document length
            execute_batch_update_captions(cursor, data_to_update_caption)
            
            # Commit after processing each chunk
            conn.commit()

conn.commit()
cursor.close()