import csv
import math
import sys

import networkx as nx
from tqdm import tqdm


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

            return self.ids[title_]

    # holds the translation between titles and id numbers.
    # numbers take up less space in memory than titles
    ids = Ids()

    with (open(wiki_file) as wiki_reader,
          open(links_file, 'w') as links_writer):

        for j, line in enumerate(tqdm(wiki_reader, desc='Reading Wikipedia')):

            # set this true if wanting quick test
            early_stop = False
            if early_stop and j > 10000:
                break

            # find out if there's a title on this line
            if "<title>" in line and "</title>" in line:
                start_tag_pos = line.find("<title>")
                end_tag_pos = line.find("</title>")
                title = line[start_tag_pos + 7: end_tag_pos]
                title_id = ids.get(title)

            # we now want to check if there's a link on this line.
            #
            # iterate over the characters in the line:
            #   - once we encounter matching "[[" and "]]",
            #     we process this link (if it's not a file)
            #   - if we encounter nested brackets, we reset the
            #     count as links cannot be nested
            counter = 0
            start_pos = 0
            for i, char in enumerate(line):
                if char == '[':
                    if counter == 2:
                        # we found nested brackets, start again
                        counter = 0
                    if counter == 0:
                        start_pos = i
                    counter += 1
                if char == ']':
                    counter -= 1
                    if counter == 0:
                        # we found a matching pair of brackets!

                        # strip the brackets
                        link = line[start_pos: i+1]
                        link = link[2: -2]

                        # if there's a display name, remove it
                        if '|' in link:
                            link = link.split('|')[0]

                        # check this isn't a file!
                        if link and "File:" not in link:
                            link_id = ids.get(link)
                            links_writer.write(str(title_id) + ',' + str(link_id) + '\n')

    # finally, write save all the IDs with corresponding page names
    with open(id_file, 'w') as ids_writer:
        for _id in tqdm(ids.ids, desc='Writing IDs file'):
            ids_writer.write('"' + _id + '",' + str(ids.get(_id)) + "\n")


def page_rank(id_file, links_file, results_file):
    print('Reading links...')
    graph = nx.read_edgelist(links_file, create_using=nx.DiGraph, delimiter=',')

    print('Calculating pagerank...')

    results = algorithm(graph)

    # read ids file
    ids = dict()
    with open(id_file) as id_reader:
        csv_reader = csv.reader(id_reader, delimiter=',')
        for title, _id in csv_reader:
            ids[str(_id)] = title

    # write page rank results with original page names
    with open(results_file, 'w') as results_writer:
        for page in tqdm(results, desc='Writing results file'):
            results_writer.write('"' + ids[page] + '",' + str(results[page]) + '\n')


def algorithm(graph: nx.DiGraph, d=0.85, stopping=1e-10):
    n = len(graph)
    initial = 1 / n
    for node in graph.nodes:
        graph.nodes[node]['pr'] = [initial, -1]

    # this function checks if the stopping requirement has been reached
    def stop():
        total = 0
        for node in graph:
            current_value = graph.nodes[node]['pr'][current]
            previous_value = graph.nodes[node]['pr'][not current]
            total += (current_value - previous_value) ** 2
        return math.sqrt(total) < stopping

    # apply page rank algorithm until convergence
    current = True
    iteration = 0
    while not stop():
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


def main():
    try:
        wiki_file = sys.argv[1]
        id_file = sys.argv[2]
        links_file = sys.argv[3]
        results_file = sys.argv[4]
    except IndexError:
        print('Usage: python [wiki file] [id file] [links file] [results file]')
        sys.exit(1)

    scrape_links(wiki_file, id_file, links_file)
    page_rank(id_file, links_file, results_file)


if __name__ == "__main__":
    main()
