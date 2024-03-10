import re
from nltk.stem.porter import *
import time
import math
from bs4 import BeautifulSoup

#Functions for preprocessing

def tokenisation2(string):
    """
    Tokenizes the input string, removing non-alphanumeric characters and empty lines.

    Args:
        string (str): Input text to tokenize.

    Returns:
        list of str: List of tokens.
    """
    
    tokens_list = []

    new_line = re.sub("[^a-zA-Z0-9]", " ", string)
    new_line = ' '.join(new_line.split()) #get ride of multiple whitespaces in a row
    tokens = new_line.strip().split(" ")
    if tokens != ['']: #get rid of empty lines
        tokens_list += tokens

    return tokens_list

def lowercase(tokens_list):
    """
    Converts a list of tokens to lowercase.

    Args:
        tokens_list (list of str): List of tokens.

    Returns:
        list of str: List of lowercase tokens.
    """

    return [x.lower() for x in tokens_list] 

def load_stop_words(file_name):
    """
    Loads a set of stop words from a file.

    Args:
        file_name (str): Path to the file containing stop words.

    Returns:
        set: Set of stop words for faster lookup.
    """

    stop_words = []
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        for l in f.readlines():
            stop_words.append(l.strip())
        
    return set(stop_words)

def remove_stop_words(tokens_list, stop_words):
    """
    Removes stop words from a list of tokens.

    Args:
        tokens_list (list of str): List of tokens.
        stop_words (set): Set of stop words.

    Returns:
        list of str: List of tokens with stop words removed.
    """

    return [x for x in tokens_list if x not in stop_words]

def stemming(tokens_list):
    """
    Applies stemming to a list of tokens using the Porter Stemmer.

    Args:
        tokens_list (list of str): List of tokens.

    Returns:
        list of str: List of stemmed tokens.
    """

    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens_list]

#load stop words set
stop_words = load_stop_words("ttds_2023_english_stop_words.txt")

# Index creation
def add_tokens_to_index(tokens, doc_id, index_dict):
    """
    Add tokens to the index dictionary, associating them with document IDs and positions.

    Args:
        tokens (list of str): List of tokens to add to the index.
        doc_id (int): Document ID.
        index_dict (dict): The index dictionary.

    Returns:
        None
    """
    
    for position, token in enumerate(tokens):
        if token not in index_dict:
            index_dict[token] = {doc_id: [position]}
        else:
            if doc_id in index_dict[token]:
                index_dict[token][doc_id].append(position)
            else:
                index_dict[token][doc_id] = [position]


def create_index_from_xml(file_path, doc_element_name = "DOC", doc_nr_name = "DOCNO", relevant_info_tags = ["TEXT","HEADLINE"]):
    """
    Create an index from an XML file containing document elements.

    This function parses an XML file, extracts relevant text content from specified tags,
    preprocesses the text, and constructs an index containing terms and their document positions.

    Parameters
    ----------
    file_path : str
        The path to the XML file to be indexed.
    doc_element_name : str, optional
        The XML tag name for document elements (default is "DOC").
    doc_nr_name : str, optional
        The XML tag name for document numbers (default is "DOCNO").
    relevant_info_tags : list of str, optional
        A list of XML tag names that contain relevant text content (default is ["TEXT", "HEADLINE"]).

    Returns
    -------
    dict
        An index dictionary containing terms and their associated document positions.

    Notes
    -----
    - The function tokenizes, converts to lowercase, removes stop words, and applies stemming to the text content.
    - The resulting index maps terms to document IDs and positions.
    """
    index_dict = {}
    
    with open(file_path, 'r') as file: #trec.
        xml_file = file.read()

        soup = BeautifulSoup(xml_file, 'xml')
        doc_elements = soup.find_all(doc_element_name)

        for doc in doc_elements:

            doc_index = int(doc.find(doc_nr_name).get_text())

            for element_type in relevant_info_tags:
                text_element = doc.find(element_type)
                text = text_element.get_text() if text_element else ""

                if text_element: #are there any xml elements with element_type?
                    #tokenize
                    list_ = tokenisation2(text)
                    #lowercase
                    list_ = lowercase(list_)
                    #stopping
                    list_ = remove_stop_words(list_, stop_words)
                    #stemming
                    list_ = stemming(list_)

                    #add to index dict
                    add_tokens_to_index(list_, doc_index, index_dict)
                    
    return index_dict

#trec_5000_index = create_index_from_xml('cw1collection/trec.5000.xml')

#save index for later usage
def save_index_to_txt(index_dict, txt_path):
    """
    Save the index to a text file in a specific format.

    Args:
        index_dict (dict): The index dictionary.
        txt_path (str): Path to the output text file.

    Returns:
        None
    """

    with open(txt_path, "w") as f:
        for term, nested in sorted(index_dict.items()):
            print(f'{term}:', file=f)
            
            for doc_id, positions in nested.items():
                string_positions = ','.join(map(str, positions))
                print(f'    {doc_id}: {string_positions}', file=f)
                
            print(file=f)
        print(file=f)

#save index in the required format
def save_index_to_txt_with_df(index_dict, txt_path):
    """
    Save the index with document frequency information to a text file.

    Args:
        index_dict (dict): The index dictionary.
        txt_path (str): Path to the output text file.

    Returns:
        None
    """

    with open(txt_path, "w") as f:
        for term, nested in sorted(index_dict.items()):
            df = len(nested.keys())
            print(f'{term}:{df}', file=f)
            
            for doc_id, positions in nested.items():
                string_positions = ','.join(map(str, positions))
                print(f'\t{doc_id}: {string_positions}', file=f)
                
        print(file=f)

#load an index from a txt file
def load_index_from_txt(txt_path):
    """
    Load an index from a text file.

    Args:
        txt_path (str): Path to the input text file.

    Returns:
        dict: The loaded index dictionary.
    """

    nested_index = {}
    current_key = None
    
    with open(txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                if line.endswith(':'):
                    current_key = line[:-1]
                    nested_index[current_key] = {}
                elif current_key is not None:
                    parts = line.split(': ')
                    sub_key = int(parts[0])
                    values = list(map(int, parts[1].split(',')))
                    nested_index[current_key][sub_key] = values        
        
    return nested_index

#save_index_to_txt(trec_5000_index, "trec.5000_index.txt")
#save_index_to_txt_with_df(trec_5000_index, "index.txt")
loaded_dict = load_index_from_txt("trec.5000_index.txt")
#print(loaded_dict == trec_5000_index)


#Running search on index
class SearchEngine:
    """
    A class representing a search engine for information retrieval.

    This class allows users to perform various types of searches on an index
    containing preprocessed text data. It supports complex Boolean queries
    and ranked retrieval using TF-IDF scoring.

    Attributes
    ----------
    index : dict
        The index dictionary containing preprocessed text data with document IDs.
    stop_words : set
        A set of stop words for filtering during text preprocessing.
    unique_doc_ids : set
        A set of all unique document IDs in the index.

    Methods
    -------
    _get_all_doc_ids()
        Retrieves all unique document IDs from the index.

    _term_search(searched_term)
        Searches for documents containing a single term.

    _phrase_search(searched_phrase)
        Searches for documents containing a phrase.

    _proximity_search(searched_phrase)
        Searches for documents where terms are within a specified proximity.

    search(searched_phrase)
        Performs complex Boolean searches with AND, OR, and NOT operations.

    ranked_retrieval(searched_phrase, how_many_relevant=10)
        Ranks documents based on query terms' importance and returns the top results.

    """

    def __init__(self, index, stop_words):
        """
        Initializes a SearchEngine instance with an index and stop words.

        Parameters
        ----------
        index : dict
            The index dictionary containing preprocessed text data with document IDs.
        stop_words : set
            A set of stop words for filtering during text preprocessing.
        """

        self.index = index
        self.stop_words = stop_words
        
    def _get_all_doc_ids(self):
        """
        Retrieve all unique document IDs from the index.
        """
        unique_doc_keys = set()

        for inner_dict in self.index.values():
            unique_doc_keys.update(inner_dict.keys())

        self.unique_doc_ids = unique_doc_keys
        
    def _term_search(self, searched_term):
        """
        Search for documents containing a single term.

        Parameters
        ----------
        searched_term : str
            The term to search for.

        Returns
        -------
        set
            A set of document IDs containing the term.
        """

        #stopping
        searched_term = remove_stop_words([searched_term], self.stop_words)
        #apply stemming
        searched_term = stemming(searched_term)[0]
        if searched_term in self.index:
            return set(self.index[searched_term].keys())
        else:
            return set()
        
    def _phrase_search(self, searched_phrase):
        """
        Search for documents containing a phrase.

        Parameters
        ----------
        searched_phrase : str
            The phrase to search for.

        Returns
        -------
        set
            A set of document IDs containing the phrase.
        """
        terms = searched_phrase.replace('"', '' ).split(" ")
        terms = remove_stop_words(terms, self.stop_words)
        terms = stemming(terms)
        
        terms_dicts = []
        for term in terms:
            if term in self.index:
                terms_dicts.append(self.index[term])
            else:
                return set()
        
        results = set()
        
        #find common doc_ids
        commons_docs = set.intersection(*map(set, terms_dicts)) #starred expression
        if commons_docs == set():
            return set()
        else:
            for key in commons_docs:
                for nr, dictionary in enumerate(terms_dicts):
                    current_positions = dictionary[key]
                    if nr == 0:
                        common_positions = set(current_positions)
                    else:
                        current_positions = [number-nr for number in current_positions]
                        common_positions = common_positions.intersection(current_positions)
                
                if common_positions != set():
                    results.add(key)
                        
        return results
    
    def _proximity_search(self, searched_phrase):
        """
        Search for documents where terms are within a specified proximity.

        Parameters
        ----------
        searched_phrase : str
            The proximity query.

        Returns
        -------
        set
            A set of document IDs where terms are within the specified proximity.
        """
        #find the proximity number for the query
        proximity_num = int(re.findall(r'[0-9]+', searched_phrase)[0])
        
        #tokenize
        terms = re.sub("[^a-z ]", " ", searched_phrase)
        terms = ' '.join(terms.split())
        terms = terms.strip().split(" ")
        
        #stopping and stemming
        terms = remove_stop_words(terms, self.stop_words)
        terms = stemming(terms)
        
        terms_dicts = []
        for term in terms:
            if term in self.index:
                terms_dicts.append(self.index[term])
            else:
                return set()
        
        results = set()
        
        #find common doc_ids
        commons_docs = set.intersection(*map(set, terms_dicts)) #starred expression
        if commons_docs == set():
            return set()
        else:
            for key in commons_docs:
                for nr, dictionary in enumerate(terms_dicts):
                    current_positions = dictionary[key]
                    if nr == 0:
                        common_positions = set(current_positions)
                    else:
                        to_remove = []
                        for num1 in common_positions:
                            if all([abs(num1 - num2) > proximity_num for num2 in current_positions]):
                                to_remove.append(num1)

                        for num in to_remove:
                            common_positions.remove(num)
                
                if common_positions != set():
                    results.add(key)
                        
        return results
    
    def search(self, searched_phrase):
        """
        Perform complex Boolean searches with AND, OR, and NOT operations.
        Choose the right function for different queries.

        Parameters
        ----------
        searched_phrase : str
            The Boolean query.

        Returns
        -------
        set
            A set of document IDs matching the query.
        """

        #tokenize the query
        tokens = re.findall(r'"[^"]*"|#[0-9]+.+\)|\S+', searched_phrase) #r'"[^"]+"|\S+'

        results = []
        for term in tokens:
            if term not in ["AND", "OR", "NOT"]:
                if term.startswith('"'):
                    results.append(self._phrase_search(term.lower()))
                elif term.startswith('#'):
                    results.append(self._proximity_search(term.lower()))
                else:
                    results.append(self._term_search(term.lower()))
            else:
                results.append(term)
                
                
        #go through results using set operations
        
        #replace all nots with corresponding negated sets
        index = 0
        negated_results = []
        while index < len(results):
            if results[index] == "NOT":
                negated_results.append(self.unique_doc_ids-results[index+1])
                index += 2
            else:
                negated_results.append(results[index])
                index +=1
        
        #do AND, OR operations
        relevant_docs = negated_results[0]
        index = 1
        while index < len(negated_results):
            if negated_results[index] == "OR":
                relevant_docs = relevant_docs | negated_results[index+1]
                index += 2
            elif negated_results[index] == "AND":
                relevant_docs = relevant_docs & negated_results[index+1]
                index += 2
        
        return relevant_docs

    def ranked_retrieval(self, searched_phrase, how_many_relevant = 150):
        """
        Rank documents based on query terms' importance and return the top results.

        Parameters
        ----------
        searched_phrase : str
            The query.
        how_many_relevant : int, optional
            Number of relevant documents to return (default is 10).

        Returns
        -------
        list of tuple
            A list of (document_id, score) tuples.
        """
        
        #preprocess searched_phrase
        terms = tokenisation2(searched_phrase)
        lower_tokens = lowercase(terms)
        stopping_tokens = remove_stop_words(lower_tokens, self.stop_words)
        stemmed_tokens = stemming(stopping_tokens)
        
        number_of_all_docs = len(self.unique_doc_ids) #N for the formula
        ranked_docs = {doc_id:0 for doc_id in self.unique_doc_ids} #dict to store score results
        
        #sum importance over terms
        for token in stemmed_tokens:
            #df(t): number of documents term t appeared in
            df_t = len(self.index[token].keys())
            if df_t != 0:
                idf_t = math.log((number_of_all_docs/df_t),10)
            else:
                idf_t = 0
                
            #calculate tf(t,d) and combine with idf(t)
            idftf = {key:((1+math.log(len(value),10))*idf_t) for (key,value) in self.index[token].items()}   
            
            #sum results with previous
            for key in idftf:
                ranked_docs[key]+= idftf[key]
                
        ranked_docs_non_zero = {key:'{:.4f}'.format(round(value,4)) for key, value in ranked_docs.items() if value != 0}
        
        if len(ranked_docs_non_zero) <= how_many_relevant:
            return sorted(ranked_docs_non_zero.items(), key=lambda x:x[1], reverse=True)
        else:
            return sorted(ranked_docs_non_zero.items(), key=lambda x:x[1], reverse=True)[0:how_many_relevant]


trec_search_engine = SearchEngine(loaded_dict, stop_words)
trec_search_engine._get_all_doc_ids()


def read_queries(file_path):
    """
    Read and parse query data from a file.

    Args:
        file_path (str): Path to the query data file.

    Returns:
        dict: A dictionary of query data.
    """
    results = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            key, value = parts[0].strip(), parts[1].strip()
            results[key] = value                    

    return results

def save_boolean_to_txt(file_path, relevant_docs_set, query_nr):
    """
    Save the results of Boolean queries to a text file.

    Args:
        file_path (str): Path to the output text file.
        relevant_docs_set (set): Set of relevant document IDs.
        query_nr (str): Query number or identifier.

    Returns:
        None
    """
    with open(file_path, "a") as f:
        for doc_id in relevant_docs_set:
            print(f'{query_nr},{doc_id}', file=f)

#check boolean queries
data = read_queries("cw1collection/queries.boolean.txt")
for key, value in data.items():
    print(key)
    print(trec_search_engine.search(value))
    save_boolean_to_txt("results.boolean.txt", trec_search_engine.search(value), key)

def save_ranked_to_txt(file_path, ranked_list, query_nr):
    """
    Save the results of ranked queries to a text file.

    Args:
        file_path (str): Path to the output text file.
        relevant_docs_set (set): Set of relevant document IDs.
        query_nr (str): Query number or identifier.

    Returns:
        None
    """
    with open(file_path, "a") as f:
        for tuple_ in ranked_list:
            print(f'{query_nr},{tuple_[0]},{tuple_[1]}', file=f)

#checked ranked queries
data = read_queries("cw1collection/queries.ranked.txt")
results_dict = {}
for key, value in data.items():
    print(key)
    results_dict[key] = (trec_search_engine.ranked_retrieval(value))    
    print(results_dict[key])
    save_ranked_to_txt("results.ranked.txt", results_dict[key], key)
