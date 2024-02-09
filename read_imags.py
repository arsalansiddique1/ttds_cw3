import re
import csv

file_path = 'enwiki-latest-pages-articles1.xml-p1p41242/short.xml'

image_pattern = re.compile(r'\[\[File:(.*?)\]\]')

csv_file_path = 'images_with_captions.csv'

with open(file_path, 'r', encoding='utf-8') as file, \
     open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filenames', 'captions'])

    for line in file:
        matches = image_pattern.findall(line)
        for match in matches:
            # Split the match into filename and the rest of the content
            parts = match.split('|', 1)
            filename = parts[0]
            #caption = parts[1] if len(parts) > 1 else ''
            # Write to the CSV file
            csv_writer.writerow([filename, line.strip()])
            #print(f'Filename: {filename}, Caption: {caption}')
