from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from ranked_search_db import ranked_search_db
from boolean_search_db import bool_search_db

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

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI app"}

@app.get("/search")
def search(query: str, queryExpansion: bool = False):
    # Implement search logic here
    if queryExpansion:
        #ARSALAN CODE HERE
        #call your function
        #call ranked_search_db(modified_query)
        return {"results": None}
    else:
        #DEFAULT: DO NOT CHANGE
        results = ranked_search_db(query)
    return {"results": results}

@app.get("/boolean_search")
def boolean_search(query: str):
    # Implement search logic here
    results = bool_search_db(query)
    return {"results": results}
