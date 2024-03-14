from transformers import pipeline
import pandas as pd
import time
from keywords_extraction import *


# Load the dataset
#df = pd.read_csv('dataset.csv')

classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")


query = "pakistan and it's people"
start_time = time.perf_counter()  # Start timing
keywords = extract_keywords(query)

for keyword in keywords:
    synonym_list = find_synonyms(keyword)
    if synonym_list:
        if (len(synonym_list) > 5):
            result = classifier(query, synonym_list[:5], multi_label = True)
            print(result)
        else:
            result = classifier(query, synonym_list[:5], multi_label = True)
            print(result)
            
    
end_time = time.perf_counter()  # End timing
duration = end_time - start_time  # Calculate duration
print(f"Classification time: {duration:.6f} seconds")



#result = classifier(query, class_descriptions, multi_label = True)




