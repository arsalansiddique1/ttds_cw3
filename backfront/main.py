from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from dotenv import load_dotenv
from ranked_search_db import ranked_tfidf_search, retrieve_image_data

# # Load environment variables from the .env file
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

print("xxxx")
print(DB_NAME)
print(DB_USER)
print(DB_PASSWORD)
print(DB_HOST)


MAX_NUM_RESULTS = 500

# Function to search PostgreSQL database
def ranked_search(query):
    tfidfs = ranked_tfidf_search(query)
    sorted_results = sorted(tfidfs, key=tfidfs.get, reverse=True)[:MAX_NUM_RESULTS]
    image_data = retrieve_image_data(sorted_results)
    results = [image_data[int(i)] for i in sorted_results if int(i) in image_data]

    return results


@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI app"}

@app.get("/search")
#def search(query: str):
def search():
    # Implement search logic here
    results = ranked_search("cat")
    return {"results": results}

# @app.get("/test")
# def test():
#     conn = psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST
#     )
#     cursor = conn.cursor()
#     sql = "SELECT * FROM captions2 WHERE id=1;"

#     # Execute the query with the list of terms as a parameter
#     cursor.execute(sql)

#     # Fetch all rows
#     matching_rows = cursor.fetchall()

#     # Close connection
#     conn.close()

#     results = matching_rows

#     return {"results": results}