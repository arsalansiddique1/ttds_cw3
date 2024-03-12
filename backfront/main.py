from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from ranked_search_db import ranked_tfidf_search, ranked_search

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
def search(query: str):
    # Implement search logic here
    results = ranked_search(query)
    return {"results": results}

@app.get("/boolean_search")
def boolean_search(query: str):
    # Implement search logic here
    return None
