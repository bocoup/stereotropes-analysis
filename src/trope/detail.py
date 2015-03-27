# Builds detail files for each film
#
# python -m src.trope.detail --dest=/Users/iros/dev/bocoup/tvtropes/data/tropes/detail
#   --extended=True

from os.path import join
from src import util
from src.trope import util as tropeutil
from src.trope import similar
from src.trope import trope_dictionary as t_dict

def write_tropes(tropes, dest):
  for trope in tropes.values():
    util.write_json(join(dest, trope['id'] + '.json'), trope)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Individual trope files')
    parser.add_argument('--dest', help='Destination folder', required=True)

    args = parser.parse_args()

    films = util.read_json('data/results/films/full_with_similarity.json')

    male_adj_ll = util.read_json('data/analysis/trope_ll-male.json')
    female_adj_ll = util.read_json('data/analysis/trope_ll-female.json')

    male_trope_adj = util.read_json('data/results/tropes_adjectives-male.json')
    female_trope_adj = util.read_json('data/results/tropes_adjectives-female.json')

    male_trope_films = util.read_json('data/results/films/trope_films-male.json')
    female_trope_films = util.read_json('data/results/films/trope_films-female.json')

    film_categories = util.read_json('data/results/films/categories.json')

    # build extended info tropes
    tropes = t_dict.build_tropes()
    tropes = t_dict.extended_info(tropes)

    # add adjectives and their ll scores
    tropes_with_adjectives = tropeutil.get_adjective_scores(tropes, male_adj_ll, female_adj_ll)

    # get related tropes to the adjectives
    tropes_with_adjective_tropes = tropeutil.get_adjective_related_tropes(tropes_with_adjectives, male_trope_adj, female_trope_adj)

    # get trope variance over time
    tropes_with_occurance_over_time = tropeutil.get_occurance_over_time(tropes, male_trope_films, female_trope_films, film_categories)

    # tropes with similarity
    tropes_with_similarity = similar.get_similar_tropes(tropes_with_occurance_over_time, films)

    write_tropes(tropes_with_similarity, args.dest)
