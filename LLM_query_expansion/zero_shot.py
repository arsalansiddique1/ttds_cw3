from transformers import pipeline
import pandas as pd

# Load the dataset
df = pd.read_csv('dataset.csv')

classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli")


#class_labels = df['labeltext'].unique().tolist()
class_descriptions = ["pets", "cats", "dogs", "animals", "lions", "dolphins"]
query = "a lazy cat"

result = classifier(query, class_descriptions, multi_label = True)

print(result)

