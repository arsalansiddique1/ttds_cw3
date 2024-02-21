import csv
import hashlib
import urllib.parse
import psycopg2
import os
from dotenv import load_dotenv
import time

# Specify the absolute path to the .env file
#dotenv_path = './.env'

# Load environment variables from the .env file
load_dotenv()

# Functions for CSV load
def load_csv_to_dict_list(csv_file):
    data = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter= "\t")
        for row in reader:
            row["filenames"] = row["filenames"].replace(" ", "_")
            data.append(row)
    return data

def url_from_filenames(data):
    modified_data = []
    url_start = "https://upload.wikimedia.org/wikipedia/commons/"
    for entry in data:
        mod_entry = entry.copy()
        decoded = urllib.parse.unquote(mod_entry["filenames"])
        md5_hash = hashlib.md5(str(decoded).encode('utf-8')).hexdigest()
        file_name = mod_entry["filenames"]
        mod_entry["filenames"] = f"{url_start}{md5_hash[0]}/{md5_hash[0:2]}/{file_name}"
        modified_data.append(mod_entry)
    return modified_data

# Function to create and populate PostgreSQL database
def create_postgres_database(data):
    DB_NAME = os.getenv("DBNAME")
    DB_USER = os.getenv("DBUSER")
    DB_PASSWORD = os.getenv("DBPASSWORD")
    DB_HOST = os.getenv("DBHOST")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS your_table_name
                    (id SERIAL PRIMARY KEY,
                    url TEXT,
                    caption TEXT)''')

    # Benchmarking
    start_time = time.time()

    # Insert data into table
    for row in data:
        cursor.execute('''INSERT INTO your_table_name (url, caption)
                        VALUES (%s, %s)''', (row["filenames"], row["captions"]))
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken for loop execution: {execution_time} seconds")

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Database created and populated successfully.")

# csv_file = 'images_with_captions.csv'
# raw_data = load_csv_to_dict_list(f".\caption_extraction\{csv_file}")
# data = url_from_filenames(raw_data)
# create_postgres_database(data)


#simple example
# Read database credentials from environment variables
# DB_NAME = os.getenv("DBNAME")
# DB_USER = os.getenv("DBUSER")
# DB_PASSWORD = os.getenv("DBPASSWORD")
# DB_HOST = os.getenv("DBHOST")

# # # Function to search PostgreSQL database
# def search_db(query):
#     conn = psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST
#     )
#     cursor = conn.cursor()

#     # Query PostgreSQL database
#     cursor.execute('''SELECT * FROM your_table_name WHERE caption ILIKE %s''', ('%' + query + '%',))
#     columns = [desc[0] for desc in cursor.description]  # Get column names
#     results = [dict(zip(columns, row)) for row in cursor.fetchall()]

#     # Close connection
#     conn.close()

#     return results

# print(search_db("flag of pakistan"))

#returns
#[{'id': 17, 'url': 'https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg', 'caption': 'Flag of Pakistan'},
#  {'id': 1793, 'url': "https://upload.wikimedia.org/wikipedia/commons/f/ff/Flag_of_Pakistan_People's_Party.svg", 'caption': 'The Flag of Pakistan.'}]