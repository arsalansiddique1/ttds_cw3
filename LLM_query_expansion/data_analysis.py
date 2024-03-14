import pandas as pd

# Load the dataset
df = pd.read_csv('dataset.csv')

# Calculate the number of unique classes in specified columns
unique_c2 = df['c2'].nunique()
unique_c3 = df['c3'].nunique()
unique_c4 = df['c4'].nunique()
unique_labeltext = df['labeltext'].nunique()

# Print the number of unique classes
print(f"Unique classes in 'c2': {unique_c2}")
print(f"Unique classes in 'c3': {unique_c3}")
print(f"Unique classes in 'c4': {unique_c4}")
print(f"Unique classes in 'labeltext': {unique_labeltext}")
class_labels = df['labeltext'].unique().tolist()

# Now, class_labels contains all unique class labels
print(class_labels)