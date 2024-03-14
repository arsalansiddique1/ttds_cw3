from transformers import pipeline
import pandas as pd
import time
from keywords_extraction import *


# Load the dataset
#df = pd.read_csv('dataset.csv')

classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")


query = "a lazy cat"
start_time = time.perf_counter()  # Start timing
keywords = extract_keywords(query)
rel_terms = []
for keyword in keywords:
    synonym_list = find_synonyms(keyword)
    if synonym_list:
        if (len(synonym_list) > 5):
            result = classifier(query, synonym_list[:5], multi_label = True)
            rel_terms.append(result['labels'][0])
        else:
            result = classifier(query, synonym_list[:5], multi_label = True)
            rel_terms.append(result['labels'][0])
            
    
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Classification time: {duration:.6f} seconds")
print(rel_terms)



#result = classifier(query, class_descriptions, multi_label = True)




