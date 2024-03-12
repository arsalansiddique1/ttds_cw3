import psycopg2
import json
from index_operations import read_json_file
# Function to insert data into PostgreSQL
def insert_data_from_json(json_data, conn):
    try:
        cur = conn.cursor()
        
        # Insert into 'documents' table first
        if '_doc_lengths' in json_data:
            for file, length in json_data['_doc_lengths'].items():
                cur.execute("INSERT INTO documents (file, length) VALUES (%s, %s) ON CONFLICT (file) DO NOTHING;", (file, length))

        # Then insert into 'terms' table and 'postings' table
        for term, info in json_data.items():
            if term != '_doc_lengths':
                df = info['df']
                cur.execute("INSERT INTO terms (term, document_frequency) VALUES (%s, %s) ON CONFLICT (term) DO NOTHING;", (term, df))
                
                for file, positions in info['postings'].items():
                    positions_array = '{' + ','.join(map(str, positions)) + '}'
                    cur.execute("INSERT INTO postings (term, file, positions) VALUES (%s, %s, %s) ON CONFLICT (term, file) DO NOTHING;", (term, file, positions_array))

        conn.commit()
        cur.close()
        print("Data inserted successfully into PostgreSQL")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback the transaction on error


def query_and_display_data(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        
        for row in rows:
            print(row)
            
        cur.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Database connection parameters
dbname = 'invertedindices'
user = 'postgres'
password = 'password'
host = 'localhost'  # or another hostname if your DB is remote

# SQL statements to create tables
create_terms_table = """
CREATE TABLE IF NOT EXISTS terms (
    term TEXT PRIMARY KEY,
    document_frequency INTEGER NOT NULL
);
"""

create_documents_table = """
CREATE TABLE IF NOT EXISTS documents (
    file TEXT PRIMARY KEY,
    length INTEGER NOT NULL
);
"""

create_postings_table = """
CREATE TABLE IF NOT EXISTS postings (
    term TEXT NOT NULL,
    file TEXT NOT NULL,
    positions INTEGER[] NOT NULL,
    PRIMARY KEY (term, file),
    FOREIGN KEY (term) REFERENCES terms(term),
    FOREIGN KEY (file) REFERENCES documents(file)
);
"""
b_tree_idx_terms = """
CREATE INDEX idx_terms_term ON terms(term);
"""
b_tree_idx_file = """
CREATE INDEX idx_documents_file ON documents(file);
"""

json_data = read_json_file('index.json')

try:
    # Connect to your database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Execute SQL commands
    cur.execute(create_terms_table)
    cur.execute(create_documents_table)
    cur.execute(create_postings_table)

    # Insert data into PostgreSQL
    #insert_data_from_json(json_data, conn)
    
    #Creates b-tree indexes for term column to optimise df lookups
    #cur.execute(b_tree_idx_terms)
    #Will speed up lookup of document lengths
    #cur.execute(b_tree_idx_file)
    
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
    cur.close()
    conn.close()
    
    print("Tables created successfully")
except Exception as e:
    print(f"An error occurred: {e}")
