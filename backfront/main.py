from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#functions for csv load
import hashlib
import urllib.parse
import csv

def load_csv_to_dict_list(csv_file):
    data = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
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

#load data
csv_file = 'images_with_captions.csv'
raw_data = load_csv_to_dict_list(csv_file)
data = url_from_filenames(raw_data)

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
    results = [result for result in data if query.lower() in result["captions"].lower()]
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