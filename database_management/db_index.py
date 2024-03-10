import psycopg2
import os
from utils import preprocess_text, extract_stopwords


# Connect to PostgreSQL database
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
cursor = conn.cursor()
cur2 = conn.cursor()

print(DB_HOST,DB_NAME,DB_PASSWORD,DB_USER)

#load stopwords
stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

# Iterate through caption table
cursor.execute("SELECT id, caption FROM captions2_copy")
row = cursor.fetchone()
while row:
    # Process the row
    terms_encountered = []
    document_id, caption = row
    cap_tokens = preprocess_text(caption, stopwords)

    # Calculate document length
    document_length = len(cap_tokens) 

    print(document_id)
    break
    
    # # Update document length in caption table
    # cur2.execute("UPDATE captions2_copy SET doc_length = %s WHERE id = %s", (document_length, document_id))
    # conn.commit()
    
    # # Update terms table and middle table
    # for pos, term in enumerate(cap_tokens):
    #     # Update document frequency in terms table
    #     if term not in terms_encountered:
    #         cur2.execute("INSERT INTO terms (term, doc_frequency) VALUES (%s, 1) ON CONFLICT (term) DO UPDATE SET doc_frequency = terms.doc_frequency + 1", (term,))
    #         conn.commit()
    #         terms_encountered.append(term)
        
    #     # Insert into middle table
    #     cur2.execute("INSERT INTO middle (id, term, position) VALUES (%s, %s, %s)", (document_id, term, pos))
    #     conn.commit()

    # Fetch the next row
    row = cursor.fetchone()

    # #keep track of progress
    # if document_id in [10, 100, 1000, 10000, 100000, 1000000, 2000000, 3000000, 4000000, 5000000]:
    #     print("Passed doc id nr:", document_id)

# Commit the changes and close the connection
conn.commit()
conn.close()