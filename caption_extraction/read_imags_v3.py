import sys

from mwparserfromhtml import HTMLDump
import re
from itertools import filterfalse
from nltk.stem import PorterStemmer
from tqdm import tqdm

html_file_path = sys.argv[1]
html_dump = HTMLDump(html_file_path)

import connect_connector
import sqlalchemy

db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()

from hashlib import md5

curr_max = 2606841  # == select max(id) from captions2;

image_id = curr_max + 1 # start counting after last index.

last_db_title = "Glencoe Station"
add_to_db = False

with db.connect() as conn:

    stmt = sqlalchemy.text(
        "INSERT INTO captions2 (id, filename, title, caption) VALUES (:id, :filename, :title, :caption)"
    )

    for article in tqdm(html_dump):
        title = article.get_title()
        
        if add_to_db:
            for image in article.html.wikistew.get_images():

                if image.caption != "":     #only include images with a caption
                    filename = image.title
                    f_hash = md5(filename.encode()).hexdigest()
                    file_loc = f_hash[0:1] + '/' + f_hash[0:2] + '/' + filename

                    caption = image.caption

                    conn.execute(stmt, parameters=
                        {"id": image_id, "filename": file_loc, "title": title, "caption": caption}
                    )
                    conn.commit()

                    image_id += 1
        
        if title == last_db_title:    #start adding articles after last article
            add_to_db = True