# Current Optimizations implemented

## V0.1.0
- Added a timer to measure how quickly query takes for boolean, proximity and phase search
- Fixed the load_index_from_file function and 3 main searches are now working 

### TODOs
- Impelement TF-IDF scoring
- Try out compression techniques to reduce the size of the inverted index






# Potential Further Indexing Optimizations

## Term Frequency–Inverse Document Frequency (TF-IDF) Weighting:
Integrate TF-IDF scoring to prioritize terms that are more unique to a document, improving the relevance of search results.
## Compression Techniques:
Apply index compression methods (e.g., variable byte coding, Elias gamma coding) to reduce the size of your positional inverted index, optimizing memory usage and potentially speeding up search operations.
## Stemming and Lemmatization:
Implement stemming or lemmatization to consolidate variations of words to their root form, reducing index size and improving match accuracy.
## Stop Words Filtering:
Enhance your stop words list and implement filtering to exclude common words from the index, streamlining the index and focusing on more meaningful terms.
## Partitioned Indexes:
Consider partitioning your index based on criteria like document type or content category to speed up query processing by searching through a smaller, more relevant subset of the index.
## Index Sharding:
Distribute the index across multiple machines or storage systems (sharding) to improve scalability and parallelize query processing. (hard) 

# Potential Additional Search Functionalities

## Ranked Retrieval:
Implement a ranking algorithm (e.g., BM25, vector space model) to order search results by relevance based on query term frequency, document length, and other factors.
## Synonym Expansion:
Integrate a thesaurus or use word embeddings to expand queries with synonyms, capturing a broader range of relevant documents.
## Faceted Search:
Allow users to refine search results based on faceted categories (e.g., date, location, image type), enhancing the search experience.
## Spell Check and Query Suggestions:
Offer spell correction and query suggestions based on common searches or similar terms, improving usability.
## Semantic Search:
Utilize NLP and machine learning models to understand the context and semantic meaning of queries, matching based on conceptual relevance rather than exact term matches.
## Image Feature Extraction and Search:
Extend the search functionality beyond text to include image features (e.g., color, shape) using computer vision techniques, enabling more diverse query types.


