# Query Expansion:
# -Dictionary/word embedding

from gensim.models import KeyedVectors
import gensim.downloader as api

# Download the Word2Vec model trained on Google News corpus
word_vectors = api.load('word2vec-google-news-300')


# Load pre-trained Word2Vec embeddings
word_vectors = KeyedVectors.load_word2vec_format(word_vectors, binary=True)

def expand_query_with_embeddings(query, top_n=3):
    expanded_query = set(query)  # Start with original query terms
    for term in query:
        similar_terms = word_vectors.most_similar(term, topn=top_n)
        expanded_query.update([similar_term for similar_term, _ in similar_terms])
    return list(expanded_query)

# Example usage:
original_query = ['car', 'engine']
expanded_query = expand_query_with_embeddings(original_query)
print(expanded_query)
