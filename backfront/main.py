from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

#backend
app = FastAPI()

#that might be dangerous, restrict later allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Read database credentials from environment variables
DB_NAME = os.getenv("DBNAME")
DB_USER = os.getenv("DBUSER")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST")

# Function to search PostgreSQL database
def search_db(query):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = conn.cursor()

    # Query PostgreSQL database
    cursor.execute('''SELECT * FROM your_table_name WHERE caption ILIKE %s''', ('%' + query + '%',))
    columns = [desc[0] for desc in cursor.description]  # Get column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Close connection
    conn.close()

    return results


@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI app"}

@app.get("/search")
def search(query: str):
    # Implement search logic here
    results = search_db(query)
    return {"results": results}


# sample_data = [
#     {"title": "Sample Result 1", "description": "Description of Sample Result 1", "url": "https://example.com/sample1"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"},
#     {"title": "Sample Result 2", "description": "Description of Sample Result 2", "url": "https://example.com/sample2"}
# ]