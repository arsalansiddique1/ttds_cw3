import json
from index_operations import read_json_file, save_index_to_json, create_positional_inverted_index
from utils import preprocess_text, extract_stopwords
# On cloud
import connect_connector
import sqlalchemy
from sqlalchemy import text
from connect_connector import connect_with_connector

# Connect to your database
db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()
stopwords = extract_stopwords("ttds_2023_english_stop_words.txt")

### Read captions2; process and index
def read_database_file(stopwords):
    with db.connect() as conn:
        # Query the captions2 table
        # Create a SQLAlchemy text object with the SQL query
        query = sqlalchemy.text("SELECT * FROM captions2")
        captions2 = conn.execute(query)
        data = {}
        # Iterate through the query result
        for row in captions2:
            image_id = row[0]
            caption = row[3]
            cap_tokens = preprocess_text(caption, stopwords)
            if image_id in data:
                data[image_id].append(cap_tokens)
            else:
                data[image_id] = [cap_tokens]
    return data

captions_by_file = read_database_file(stopwords)
positional_index = create_positional_inverted_index(captions_by_file)
# Save index dict straight to database
#save_index_to_json(positional_index, 'index.json')

### Store the index in database
# Function to insert index(dict) into database tables
def insert_data_from_dict(data, conn):
    try:
        # Insert into 'documents' table first
        if '_doc_lengths' in data:
            for file, length in data['_doc_lengths'].items():
                conn.execute("INSERT INTO documents (file, length) VALUES (%s, %s) ON CONFLICT (file) DO NOTHING;", (file, length))

        # Then insert into 'terms' table and 'postings' table
        for term, info in data.items():
            if term != '_doc_lengths':
                df = info['df']
                conn.execute("INSERT INTO terms (term, document_frequency) VALUES (%s, %s) ON CONFLICT (term) DO NOTHING;", (term, df))
                
                for file, positions in info['postings'].items():
                    positions_array = '{' + ','.join(map(str, positions)) + '}'
                    conn.execute("INSERT INTO postings (term, file, positions) VALUES (%s, %s, %s) ON CONFLICT (term, file) DO NOTHING;", (term, file, positions_array))

        conn.commit()
        conn.close()
        print("Data inserted successfully into PostgreSQL")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback the transaction on error



# Function to insert JSON data into PostgreSQL
def insert_data_from_json(json_data, conn):
    try:
        #cur = conn.cursor()
        
        # Insert into 'documents' table first
        if '_doc_lengths' in json_data:
            for file, length in json_data['_doc_lengths'].items():
                conn.execute("INSERT INTO documents (file, length) VALUES (%s, %s) ON CONFLICT (file) DO NOTHING;", (file, length))

        # Then insert into 'terms' table and 'postings' table
        for term, info in json_data.items():
            if term != '_doc_lengths':
                df = info['df']
                conn.execute("INSERT INTO terms (term, document_frequency) VALUES (%s, %s) ON CONFLICT (term) DO NOTHING;", (term, df))
                
                for file, positions in info['postings'].items():
                    positions_array = '{' + ','.join(map(str, positions)) + '}'
                    conn.execute("INSERT INTO postings (term, file, positions) VALUES (%s, %s, %s) ON CONFLICT (term, file) DO NOTHING;", (term, file, positions_array))

        conn.commit()
        #cur.close()
        print("Data inserted successfully into PostgreSQL")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback the transaction on error


def query_and_display_data(conn, query):
    try:
        #cur = conn.cursor()
        conn.execute(query)
        rows = conn.fetchall()
        
        for row in rows:
            print(row)
            
        #cur.close()
    except Exception as e:
        print(f"An error occurred: {e}")
'''
# Database connection parameters
dbname = 'invertedindices'
user = 'postgres'
password = 'password'
host = 'localhost'  # or another hostname if your DB is remote
'''
# SQL statements to create tables
create_terms_table = sqlalchemy.text("""
CREATE TABLE IF NOT EXISTS terms (
    term TEXT PRIMARY KEY,
    document_frequency INTEGER NOT NULL
);
""")

create_documents_table = sqlalchemy.text("""
CREATE TABLE IF NOT EXISTS documents (
    file TEXT PRIMARY KEY,
    length INTEGER NOT NULL
);
""")

create_postings_table = sqlalchemy.text("""
CREATE TABLE IF NOT EXISTS postings (
    term TEXT NOT NULL,
    file TEXT NOT NULL,
    positions INTEGER[] NOT NULL,
    PRIMARY KEY (term, file),
    FOREIGN KEY (term) REFERENCES terms(term),
    FOREIGN KEY (file) REFERENCES documents(file)
);
""")
b_tree_idx_terms = sqlalchemy.text("""
CREATE INDEX IF NOT EXISTS idx_terms_term ON terms(term);
""")
b_tree_idx_file = sqlalchemy.text("""
CREATE INDEX idx_documents_file ON documents(file);
""")





try:
    with db.connect() as conn:
        # Open a cursor to perform database operations
        #cur = conn.cursor()
    
        # Execute SQL commands
        conn.execute(create_terms_table)
        conn.execute(create_documents_table)
        conn.execute(create_postings_table)

        # Insert data into PostgreSQL
        insert_data_from_dict(positional_index, conn)
        
        #Creates b-tree indexes for term column to optimise df lookups
        conn.execute(b_tree_idx_terms)
        #Will speed up lookup of document lengths
        conn.execute(b_tree_idx_file)
        
        '''
        # List tables
        cur.execute("""SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'""")
        tables = cur.fetchall()
        for table in tables:
            print(table)
        '''
        
            # Query and display data from 'terms' table
        print("Data in 'terms' table:")
        query_and_display_data(conn, "SELECT * FROM terms LIMIT 10;")

        # Query and display data from 'documents' table
        print("\nData in 'documents' table:")
        query_and_display_data(conn, "SELECT * FROM documents LIMIT 10;")

        # Query and display data from 'postings' table
        print("\nData in 'postings' table:")
        query_and_display_data(conn, "SELECT * FROM postings LIMIT 10;")
        
        
        
        # Commit the changes
        conn.commit()
        
        # Close communication with the database
        #cur.close()
        conn.close()
        
        print("Tables created successfully")
except Exception as e:
    print(f"An error occurred: {e}")
