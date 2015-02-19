# Module for producing the data for the gendertropes adjectives visualization

from src import util
from collections import defaultdict
from sets import Set
from collections import Counter
import itertools

def adj_to_tropes(trope_adjectives):
    adj_trope = defaultdict(Set)

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

# adjectives - 2 separate lists

  # gender
  # adjectives

    # id
    # name (lowercase, keep as is. keep an eye out for spaces.)
    # count (in that gender category)
    # percentage_occurance (percentage appearance in tropes in the gender category (e.g. 9% in female tropes))
    # log_likelihood (log likleyhood score)
    # tropes (associated trope list of ids)

def gender_split(male_ll, female_ll, adj_to_tropes_male, adj_to_tropes_female, total_trope_count):

    def get_percentage(adjective):
        male_tropes = []
        female_tropes =  []

        try:
            male_tropes = adj_to_tropes_male[adjective]['tropes']
        except:
            # print('keyerror male', adjective)
            None

        try:
            female_tropes = adj_to_tropes_female[adjective]['tropes']
        except:
            # print('keyerror female', adjective)
            None


        male_percent = (len(male_tropes) / float(total_trope_count)) * 100
        female_percent = (len(female_tropes) / float(total_trope_count)) * 100

        return {
            'male': male_percent,
            'female': female_percent
        }

    def get_tropes(adjective):
        male_tropes = []
        female_tropes =  []

        try:
            male_tropes = adj_to_tropes_male[adjective]['tropes']
        except:
            # print('keyerror male', adjective)
            None

        try:
            female_tropes = adj_to_tropes_female[adjective]['tropes']
        except:
            # print('keyerror female', adjective)
            None

        return {
            'male': male_tropes,
            'female': female_tropes
        }


    def format_adjectives(ll_data):
        res = []
        for tup in ll_data:
            res.append({
                'id': tup[0],
                'count': tup[1],
                'log_likelihood': tup[2],
                'log_likelihood_norm': tup[3],
                'tropes': get_tropes(tup[0]),
                'percentage_occurance': get_percentage(tup[0])
            })

        return res

    male = [adj for adj in format_adjectives(male_ll) if adj['log_likelihood'] > 0]
    female = [adj for adj in format_adjectives(female_ll) if adj['log_likelihood'] > 0]

    return {
        'male': male,
        'female': female
    }



if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Generate adjective gender split data')
    parser.add_argument('--dest', help='source file', required=True)

    args = parser.parse_args()

    male_trope_adj = util.read_json('data/results/tropes_adjectives-male.json')
    female_trope_adj = util.read_json('data/results/tropes_adjectives-female.json')

    male_ll = util.read_json('data/analysis/ll-male.json')
    female_ll = util.read_json('data/analysis/ll-female.json')

    male_tropes = util.read_json('data/results/male_tropes.json')
    female_tropes = util.read_json('data/results/female_tropes.json')

    alltropes = Set([t[0] for t in male_tropes + female_tropes])

    res = gender_split(male_ll, female_ll, adj_to_tropes(male_trope_adj), adj_to_tropes(female_trope_adj), len(alltropes))
    util.write_json(args.dest, res)




