import os
import psycopg2

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

def fetch_db_single_term(term):
    with conn.cursor() as cursor:
        sql =f"""
        SELECT * FROM terms_json WHERE term = '{term}';
        """
        cursor.execute(sql)

        matching_rows = cursor.fetchall()

        return matching_rows

def fetch_db_multiple_terms(terms):
    with conn.cursor() as cursor:
        sql =f"""
        SELECT * FROM terms_json WHERE term = ANY(%s);
        """
        # Bind the term parameter to the statement
        cursor.execute(sql, (terms,))

        matching_rows = cursor.fetchall()

        return matching_rows

def retrieve_image_data(ids):
    with conn.cursor() as cursor:
        sql = f"SELECT DISTINCT ON (title, caption) * FROM captions2 WHERE id IN %s;"

        # Execute the query with the list of IDs as a parameter
        cursor.execute(sql, (tuple(ids),))

        # Fetch all rows
        output_dict = dict()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        output_dict = {row[0]: dict(zip(columns, row)) for row in cursor.fetchall()}

        return output_dict