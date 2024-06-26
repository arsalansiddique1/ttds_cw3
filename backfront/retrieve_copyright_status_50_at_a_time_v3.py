import csv
import json, requests
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import sqlalchemy
import connect_connector
import os

# # Replace 'YOUR_ACCESS_TOKEN' with your actual personal API token
# access_token = 'ASK_IVAN_FOR_ACCESS_TOKEN_IF_NEEDED' # But I think it is not needed

# # Set up the request headers with your authorization token
# headers = {
#     'Authorization': f'Bearer {access_token}'
# }



# If we don't have info of a file, write unknown everything instead of failing
def write_unknown_file():
    return 'Unknown license', 'Unknown date', 'Unknown size', 'Unknown width', 'Unknown height'


def fetch_image_metadata_bulk(file_names):
    api_base_url = 'https://commons.wikimedia.org/w/api.php'
    titles = '|'.join([f'File:{name}' for name in file_names])
    params = {
        'action': 'query',
        'titles': titles,
        'prop': 'imageinfo',
        'iiprop': 'url|size|width|height|extmetadata',
        'format': 'json'
    }
    response = requests.get(api_base_url, params=params).json() # Add headers=headers if using with authentification
    
    name_mapping = {}

    # Populate the mapping based on the response
    if 'query' in response and 'normalized' in response['query']:
        for norm in response['query']['normalized']:
            normed_name = norm['to'].replace('File:', '')
            original_name = norm['from'].replace('File:', '')
            #name_mapping[normed_name] = original_name
            name_mapping[original_name] = normed_name
            
    pages = response['query']['pages']
    
    # Dictionary to hold the image information keyed by file name
    images_info = {}
    for page_id in pages:
        page = pages[page_id]
        # Some images might not have imageinfo if, for example, the file does not exist
        if 'imageinfo' in page:
            title = page['title'].replace('File:', '')
            images_info[title] = page['imageinfo']
        else:
            title = page['title'].replace('File:', '')
            images_info[title] = [] 
    return images_info, name_mapping



# Function with improved efficiency by adding the records 50 at a time instead of 1 at a time
def process_batch(batch, conn):
    file_names = [file_name for _, file_name in batch]
    images_info, name_mapping = fetch_image_metadata_bulk(file_names)
    records_to_insert = []
    for document_id, file_name in batch:
        lookup_name = file_name
        normalized_name = name_mapping.get(lookup_name, lookup_name)
        
                
        if normalized_name in images_info:
            try:
                license, date, file_size, width, height = extract_image_license_date_size_bulk(normalized_name, images_info)
                #print(normalized_name,license, date, file_size, width, height)
            except Exception as e:
                license, date, file_size, width, height = write_unknown_file()
                #print(f'Error in image {file_name}: {e}')
        else:
            license, date, file_size, width, height = write_unknown_file()
            #print(normalized_name,license, date, file_size, width, height)

        #print(document_id, license, date, file_size, width, height)
        records_to_insert.append({
            "id": document_id,
            "license": license,
            "date": date,
            "size": file_size,
            "width": width,
            "height": height
        })

    insert_stmt = sqlalchemy.text("""
        INSERT INTO classification_info (id, license, date, size, width, height) 
        VALUES (:id, :license, :date, :size, :width, :height)
    """)

    try:
        conn.execute(insert_stmt, records_to_insert)
        conn.commit()
    except Exception as e:
        print(f"Error inserting records: {e}")




def extract_image_license_date_size_bulk(image_name, images_info):
    if image_name in images_info and images_info[image_name]:
        image_info = images_info[image_name][0]  # Assuming there's always at least one imageinfo entry
        license = image_info.get('extmetadata', {}).get('LicenseShortName', {}).get('value', 'Unknown license')
        date_original = image_info['extmetadata'].get('DateTimeOriginal', {}).get('value', 'Unknown date')
        file_size = image_info.get('size', 'Unknown size')
        width = image_info.get('width', 'Unknown width')
        height = image_info.get('height', 'Unknown height')

        # Clean up the date
        cleaned_date = BeautifulSoup(date_original, 'html.parser').text
        cleaned_date = cleaned_date.replace('\xa0', ' ').strip()
        cleaned_date = cleaned_date.split('date QS:P', 1)[0].strip()
    
        # To solve a problem with Unknown date appearing twice in the date
        if 'Unknown dateUnknown date' in cleaned_date:
            cleaned_date = cleaned_date[12:].strip()
            
    else:
        return 'Unknown license', 'Unknown date', 'Unknown size', 'Unknown width', 'Unknown height'

    return license, cleaned_date, file_size, width, height



def fetch_and_process_images(db_engine):
    with db_engine.connect() as conn:
        offset = 2858750
        batch_size = 50
        
        while True:
            fetch_stmt = sqlalchemy.text("""
                SELECT id, filename FROM captions2_copy 
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """)
            result = conn.execute(fetch_stmt, {'limit': batch_size, 'offset': offset}).fetchall()
            if not result:
                break
            
            batch = [(row[0], '/'.join(row[1].split('/')[2:])) for row in result] # Weird syntax to ignore hash in title name and make sure that we don't remove any '/' in filename
            process_batch(batch, conn)
            offset += batch_size
            if offset % 10000 == 0:
                print(f'Processed {offset} images')
            # if offset % 1000 == 0:
            #     break
            
          
if __name__ == "__main__":
    db_engine = connect_connector.connect_with_connector()
    fetch_and_process_images(db_engine)          
            
        
        
        


        
# # OLD FUNCTION FOR CSV
# if __name__ == "__main__":
#     # Connect to the database
#     db_engine = connect_connector.connect_with_connector()

#     with open('images_with_captions.csv', 'r', encoding='utf-8') as f:
#         csv_reader = csv.reader(f)
#         next(csv_reader)  # Skip the header row
        
#         batch = []
#         for i, row in tqdm(enumerate(csv_reader)):
#             batch.append(row[0])
#             if len(batch) == 50:  # 50 is the maximum we can query at a time without getting any errors
#                 process_batch(batch, db_engine)
#                 batch = []  
            
#         if batch:  # remaining images in the last batch
#             process_batch(batch, db_engine)


### OLD FUNCTION FOR SQL LOADING EVERYTHING     
# def fetch_and_process_images(db_engine):
#     with db_engine.connect() as conn:
#         fetch_stmt = sqlalchemy.text("SELECT id, image_name FROM captions2_copy ORDER BY id") # Would pull entire table all at once
#         result = conn.execute(fetch_stmt)
        
#         batch = []
#         for row in result:
#             document_id, file_name = row['id'], row['image_name']
#             batch.append((document_id, file_name))
#             if len(batch) == 50:  # 50 is the maximum we can query at a time without getting any errors
#                 process_batch(batch, conn)
#                 batch = []
        
#         if batch:  # remaining images in the last batch
#             process_batch(batch, conn)


### Old function for writing to database, one at a time, less efficient
# def process_batch(batch, conn):
#     file_names = [file_name for _, file_name in batch]
#     images_info = fetch_image_metadata_bulk(file_names)
    
#     for document_id, file_name in batch:
#         if file_name in images_info:
#             try:
#                 license, date, file_size, width, height = extract_image_license_date_size_bulk(file_name, images_info)
#                 write_into_database_batch(conn, document_id, file_name, license, date, file_size, width, height)
#             except Exception as e:
#                 license, date, file_size, width, height = write_unknown_file()
#                 write_into_database_batch(conn, document_id, file_name, license, date, file_size, width, height)
#                 print(f'Error in image {file_name}: {e}')
#         else:
#             license, date, file_size, width, height = write_unknown_file()
#             write_into_database_batch(conn, document_id, file_name, license, date, file_size, width, height)
#             print(f'Image info not found for {file_name}')


# def write_into_database_batch(conn, document_id, file_name, license, date, file_size, width, height):
#     insert_stmt = sqlalchemy.text("""
#                 INSERT INTO wikimage (image_id, filename, license, date, size, width, height) 
#                 VALUES (:image_id, :filename, :license, :date, :size, :width, :height)
#             """)
            
#     conn.execute(insert_stmt, {
#                 "image_id": document_id,
#                 "filename": file_name,
#                 "license": license,
#                 "date": date,
#                 "size": file_size,
#                 "width": width,
#                 "height": height
#             })
