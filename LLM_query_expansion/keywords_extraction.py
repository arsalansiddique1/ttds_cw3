import spacy
from PyMultiDictionary import MultiDictionary

dictionary = MultiDictionary()


#nltk.download('wordnet')
#nltk.download('punkt')



# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

'''
def find_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():  # Ensure the original word isn't added as a synonym
                synonyms.add(lemma.name())
    return list(synonyms)
'''

def find_synonyms(word):
    return dictionary.synonym('en', word)

def extract_keywords(text):
    # Process the text
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN', 'ADJ')]
    return keywords

query = "Pakistan and it's people"
keywords = extract_keywords(query)


'''
# Example: Finding synonyms for each keyword
for keyword in keywords:
    synonym_list = find_synonyms(keyword)
    print(f"Synonyms for {keyword}: {synonym_list}")
'''

    
