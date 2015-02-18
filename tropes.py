import util

# Functions that generate trope lists for use in
# the main visualization

def all_tropes(trope_info):
    '''Return a list all the trope ids'''
    return [trope[0] for trope in trope_info]



def top_N_by_ll(n, male_ll, female_ll, male_trope_adj, female_trope_adj):
    '''Return of the top N tropes by log likelyhood.

    The log likelyhood of a trope is calculated by summing up the ll of
    adjectives found in that trope. Thus it would produce a list of the
    most distincly feminine and distincly masculine tropes. Where disctincness
    is a measure of how polarized they are.

    Half will be selected from the male list and half from the female list
    '''

    def ll_map(tuples):
        res = {}
        for tup in tuples:
            res[tup[0]] = tup[2]
        return res

    def score_trope(scores, adjs):
        res = 0
        for adj in adjs:
            res += scores[adj.lower()]
        return res

    mllmap = ll_map(male_ll)
    fllmap = ll_map(female_ll)

    male_trope_ll_scores = [(trope[0], score_trope(mllmap, trope[1])) for trope in male_trope_adj]
    female_trope_ll_scores = [(trope[0], score_trope(fllmap, trope[1])) for trope in female_trope_adj]

    male_trope_ll_scores_sorted = sorted(male_trope_ll_scores, key=lambda x: x[1], reverse=True)
    female_trope_ll_scores_sorted = sorted(female_trope_ll_scores, key=lambda x: x[1], reverse=True)

    combined = sorted(male_trope_ll_scores_sorted[0:n/2] + female_trope_ll_scores_sorted[0:n/2], key=lambda x: x[1], reverse=True)
    combined = [trope[0] for trope in combined]
    return combined


def top_N_by_film_occurrence(n, male_film_tropes, female_film_tropes):
    '''Return of the top N tropes by occurence in films

    Half will be selected from the male list and half from the female list
    '''
    def get_count(trope):
        return (trope['name'], trope['films_unique'])

    male_trope_counts = [get_count(trope) for trope in male_film_data['values']]
    female_trope_counts = [get_count(trope) for trope in female_film_data['values']]

    smtp = sorted(male_trope_counts, key=lambda x: x[1], reverse=True)
    sftp = sorted(female_trope_counts, key=lambda x: x[1], reverse=True)

    combined = sorted(smtp[0:n/2] + sftp[0:n/2], key=lambda x: x[1], reverse=True)
    combined = [trope[0] for trope in combined]
    return combined


if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Generate trope lists')
    parser.add_argument('--dest', help='source file', required=True)
    parser.add_argument('--by_film_occurence', required=False, action='store_true')
    parser.add_argument('--by_ll', required=False, action='store_true')

    args = parser.parse_args()

    male_image_info = util.read_json('data/results/images/male/results.json')
    female_image_info = util.read_json('data/results/images/female/results.json')

    male_trope_info = util.read_json('data/results/only_tropes-male.json')
    female_trope_info = util.read_json('data/results/only_tropes-female.json')

    res = []

    if args.by_ll:
        male_ll = util.read_json('data/analysis/ll-male.json')
        female_ll = util.read_json('data/analysis/ll-female.json')

        male_trope_adj = util.read_json('data/results/tropes_adjectives-male.json')
        female_trope_adj = util.read_json('data/results/tropes_adjectives-female.json')

        res = top_N_by_ll(100, male_ll, female_ll, male_trope_adj, female_trope_adj)
    elif args.by_film_occurence:
        male_film_data = util.read_json('data/results/trope_films-male.json')
        female_film_data = util.read_json('data/results/trope_films-female.json')

        res = top_N_by_film_occurrence(100, male_film_data, female_film_data)
    else:
        male_trope_info = util.read_json('data/results/only_tropes-male.json')
        female_trope_info = util.read_json('data/results/only_tropes-female.json')
        res = all_tropes(male_trope_info + female_trope_info)

    util.write_json(args.dest, res)