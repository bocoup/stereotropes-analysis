# Module for producing the data for the gendertropes adjectives visualization

import util
from collections import defaultdict
from sets import Set
from collections import Counter
import itertools
import trope_dictionary

def adj_to_tropes(male_trope_adj, female_trope_adj):
    adj_trope = defaultdict(Set)
    trope_adjectives = male_trope_adj + female_trope_adj

    for tup in trope_adjectives:
        trope_name = tup[0]
        adjectives = tup[1]
        for adjective in adjectives:
            adj_trope[adjective.lower()].add(trope_name)

    adj_trope_extended = dict()
    for k, v in dict(adj_trope).iteritems():
        adj_trope_extended[k] = {
            'adjective': k,
            'trope_count': len(v),
            'tropes': list(v)
        }

    return dict(adj_trope_extended)

def trope_to_ajd(male_trope_adj, female_trope_adj):
    trope_adj = defaultdict(Set)
    trope_adjectives = male_trope_adj + female_trope_adj

    for tup in trope_adjectives:
        trope_name = tup[0]
        adjectives = tup[1]
        for adjective in adjectives:
            trope_adj[trope_name].add(adjective.lower())

    for k, v in trope_adj.iteritems():
        trope_adj[k] = list(v)

    return dict(trope_adj)

def adjective_network(male_trope_adj, female_trope_adj, num_adjectives=100):
    adj_trope_dict = adj_to_tropes(male_trope_adj, female_trope_adj)
    trope_adj_dict = trope_to_ajd(male_trope_adj, female_trope_adj)

    sorted_adj = sorted(adj_trope_dict.values(), key=lambda x:x['trope_count'], reverse=True)

    # The adjectives for the vis and the number of tropes they appear in
    adj_nodes = [{'name': adj['adjective'], 'trope_count': adj['trope_count']} for adj in sorted_adj[0:num_adjectives]]

    # For the adjectives in the list above compute which ones
    # are connected to other adjectives based on occurrence in tropes
    adj_nodes_names = [adj['name'] for adj in adj_nodes]

    filtered_adj_trope_dict = {k : v for k, v in adj_trope_dict.iteritems() if k in adj_nodes_names}

    edge_list = []
    for adj, datum in filtered_adj_trope_dict.iteritems():
        for trope in datum['tropes']:
            # get the adjectives that appear i nthis trope and create an adjacency entry
            # the entry will be a tuple of adjectives in sorted order so we can count them
            # up later
            curr_trope_adjs = trope_adj_dict[trope]
            for target_adj in curr_trope_adjs:
                if adj != target_adj and target_adj in adj_nodes_names: #Only capture links to adjectives in the top 100
                    pair = tuple(sorted([adj, target_adj]))
                    edge_list.append(pair)


    adj_adj_links = []
    counter = Counter(edge_list)
    for item in counter:
        adj_adj_links.append({
            'source': item[0],
            'target': item[1],
            'weight': counter[item]
        })

    adj_adj_links = sorted(adj_adj_links, key=lambda x: x['weight'], reverse=True)


    # Now format the tropes to adjectives network
    trope_nodes = [datum['tropes'] for adj, datum in filtered_adj_trope_dict.iteritems()]
    trope_nodes = list(itertools.chain.from_iterable(trope_nodes))
    trope_nodes = list(Set(trope_nodes))
    trope_nodes = [{'id': trope, 'name': trope_dictionary.to_name(trope)} for trope in trope_nodes]

    trope_adj_links = []
    for trope in trope_nodes:
        trope_id = trope['id']
        for adjective in trope_adj_dict[trope_id]:
            if adjective in adj_nodes_names: #Only capture links to adjectives in the top 100
                trope_adj_links.append({'source': trope_id, 'target': adjective})


    # Return the networks

    return {
        'adj_adj_network': {
            'nodes': adj_nodes,
            'links': adj_adj_links
        },
        'trope_adj_network': {
            # 'nodes': trope_nodes,
            'links': trope_adj_links
        }
    }






if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Generate adjective info')
    parser.add_argument('--dest', help='source file', required=True)

    args = parser.parse_args()

    male_trope_adj = util.read_json('data/results/male_tropes_adjectives.json')
    female_trope_adj = util.read_json('data/results/female_tropes_adjectives.json')

    res = adjective_network(male_trope_adj, female_trope_adj)
    util.write_json(args.dest, res)