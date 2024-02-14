import re

file_path = 'enwiki-latest-pages-articles1.xml-p1p41242/enwiki-latest-pages-articles1.xml-p1p41242'

image_pattern = re.compile(r'\[\[File:(.*?)\|')


short_file = 'enwiki-latest-pages-articles1.xml-p1p41242/short.xml'

my_lines = []

i = 0
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if i < 6898060 / 10:
            i += 1
            my_lines.append(line)
        else:
            break
        
print(i)

with open(short_file, 'w', encoding='utf-8') as file:
    file.writelines(my_lines)