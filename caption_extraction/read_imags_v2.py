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

image_id = 0

with db.connect() as conn:

    stmt = sqlalchemy.text(
        "INSERT INTO captions2 (id, filename, title, caption) VALUES (:id, :filename, :title, :caption)"
    )

    for article in tqdm(html_dump):
        title = article.get_title()
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

        # if image_id == 10000:
        #     break
