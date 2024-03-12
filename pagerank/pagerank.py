import csv
import math
import random
import sys
import threading
import time

import networkx as nx
from tqdm import tqdm

from mwparserfromhtml import HTMLDump

# import connect_connector
# import sqlalchemy


# this function scrapes all the links from the wiki file
def scrape_links(wiki_file, id_file, links_file):

    # simple wrapper class for the ids dictionary
    class Ids:
        def __init__(self):
            self.ids = dict()
            self.counter = 0

        # keeps track of next available id number
        # assigns new spot in dictionary when new title encountered
        def get(self, title_):
            if title_ not in self.ids:
                self.ids[title_] = self.counter
                self.counter += 1

            return str(self.ids[title_])

    # holds the translation between titles and id numbers.
    # numbers take up less space in memory than titles
    ids = Ids()

    # wiki parser object
    wiki = HTMLDump(wiki_file)

    with open(links_file, 'w') as links_writer:

        # iterate over each article
        for i, article in enumerate(tqdm(wiki, desc='Reading Wikipedia')):

            # set this true if wanting quick test
            early_stop = False
            if early_stop and i > 10000:
                break

            # get the title of current article
            title = article.get_title()

            # iterate over all the links in the article
            for wikilink in article.html.wikistew.get_wikilinks():
                link = wikilink.title
                links_writer.write(ids.get(title) + ',' + ids.get(link) + '\n')

    # finally, write save all the IDs with corresponding page names
    with open(id_file, 'w') as ids_writer:
        for _id in tqdm(ids.ids, desc='Writing IDs file'):
            ids_writer.write('"' + _id + '"\t' + ids.get(_id) + "\n")


def page_rank(id_file, links_file, results_file):
    print('Reading links...')
    graph = nx.read_edgelist(links_file, create_using=nx.DiGraph, delimiter=',')

    print('Calculating pagerank...')

    results = algorithm(graph)

    # read ids file
    ids = dict()
    with open(id_file) as id_reader:
        csv_reader = csv.reader(id_reader, delimiter='\t')
        for title, _id in csv_reader:
            ids[str(_id)] = title

    # write page rank results with original page names
    with open(results_file, 'w') as results_writer:
        for page in tqdm(results, desc='Writing results file'):
            if page in ids:
                results_writer.write('"' + ids[page] + '"\t' + str(results[page]) + '\n')
            else:
                print("No id record for", page)


def algorithm(graph: nx.DiGraph, d=0.85, stopping=1e-14, max_iter=20):
    n = len(graph)
    initial = 1 / n
    for node in graph.nodes:
        graph.nodes[node]['pr'] = [initial, -1]

    # this function checks if the stopping requirement has been reached
    def stop():
        return False
        total = 0
        for node in graph:
            current_value = graph.nodes[node]['pr'][current]
            previous_value = graph.nodes[node]['pr'][not current]
            total += (current_value - previous_value) ** 2

        current_error = math.sqrt(total) / n

        print("Current error:", current_error)
        print("Target error:", stopping)

        return current_error < stopping

    # apply page rank algorithm until convergence
    current = True
    iteration = 0
    while not stop() and iteration < max_iter:
        iteration += 1
        print("Running page rank iteration", iteration)

        # this is algorithm from the Web Search 1 lecture slides
        for node in graph:
            graph.nodes[node]['pr'][current] = \
                ((1-d)/n
                 +
                 d * sum([graph.nodes[y]['pr'][not current]/len(list(graph.successors(y)))
                          for y in graph.predecessors(node)]))

        current = not current

    # finally, write results back to dictionary
    results = dict()
    for node in graph:
        results[node] = graph.nodes[node]['pr'][not current]

    return results

# def write_to_db(results_file):
#     # see this page for instructions to connect to DB:
#     # https://cloud.google.com/sql/docs/postgres/connect-instance-compute-engine#python
#     # IMPORTANT: MUST SET ENVIRONMENT VARIABLES FOR THIS TO WORK
#     db: sqlalchemy.engine.base.Engine = connect_connector.connect_with_connector()
#
#     with open(results_file) as results_reader, db.connect() as conn:
#         stmt = sqlalchemy.text(
#             "INSERT INTO pagerank (title, score) VALUES (:title, :score)"
#         )
#         for line in results_file:
#             title, score = line.split('\t')
#             conn.execute(stmt, parameters={"title": title, "score": score})
#             conn.commit()


def main():
    try:
        wiki_file = sys.argv[1]
        id_file = sys.argv[2]
        links_file = sys.argv[3]
        results_file = sys.argv[4]
    except IndexError:
        print('Usage: python [wiki file] [id file] [links file] [results file]')
        sys.exit(1)

    # scrape_links(wiki_file, id_file, links_file)
    page_rank(id_file, links_file, results_file)
    # write_to_db(results_file)


if __name__ == "__main__":
    main()
