import csv
import re
# Reading the csv file
def read_csv_file(file_path):
    text_dict = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            file = row['filenames']
            caption = row['captions']
            # Tokenize the caption
            cap_tokens = re.findall(r'\b[\w\']+\b', caption)
            if file in text_dict:
                text_dict[file].append(cap_tokens)
            else:
                text_dict[file] = [cap_tokens]
    return text_dict


def read_queries_from_file(filename):
    """
    Reads all the queries from a file and returns them as a list.
    """
    queries = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            query = line.strip().split(' ', 1)[1]
            queries.append(query)
  
    return queries

def write_results_to_file(results, filename):
    """
    Writes the results to a file given the dict with keys as query numbers and values as doc_ids.
    """
    with open(filename, 'w') as f:
        for query_num, doc_ids in results.items():
            for doc_id in doc_ids:
                f.write(f"{query_num},{doc_id}\n")
                
                
def write_ranked_results_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding here
        for query_num, doc_data in results.items():
            for doc_id, score in doc_data:
                f.write(f"{query_num},{doc_id},{round(score, 4)}\n")


