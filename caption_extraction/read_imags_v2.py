from mwparserfromhtml import HTMLDump
import csv
import re

html_file_path = "/Users/filipdorm/enwiki-NS0-20240201-ENTERPRISE-HTML.json.tar.gz"
html_dump = HTMLDump(html_file_path)

csv_file_path = 'images_with_captions.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:

    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['title', 'filenames', 'captions'])

    i = 0
    for article in html_dump:
        
        title = article.get_title()
        for image in article.html.wikistew.get_images():
            filename = image.title
            
            caption = image.caption
            cleaned_line =  re.sub(r'\t', '', caption)

            if image.caption != "":     #only include images with a caption
                i+=1
                csv_writer.writerow([title, filename, cleaned_line])
                print(f'Filename: {filename}, Caption: {image.caption}')

        if i == 10000:break
