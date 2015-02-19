from src import util
from os.path import splitext, basename
from src.film import util as filmutil
from src.adjectives import adjectives as adjutil


# files: only_tropes-male|female, tropes_adjectives-male, tropes_adjectives-female
def get_adjective_related_tropes(tropes, male_trope_adj, female_trope_adj):
  '''
  Returs a map of adjectives and the tropes that are related to them

  Map looks like:
  trope -> [
    [ adj1, count, ll, normalized ll, [trope1, trope2, trope3]],
    [ adj2, count, ll, normalized ll, [trope1, trope2, trope3]],
  ]
  '''

  trope_adj_dictionary = adjutil.adj_to_tropes(male_trope_adj, female_trope_adj)

  tropes_dict = {}

  for trope in tropes.values():
    name = trope['name']
    adjectives = trope['adjectives']

    for adj in adjectives:
      if adj[0] in trope_adj_dictionary:
        adj.append(trope_adj_dictionary[adj[0]]['tropes'])

    trope['adjectives'] = adjectives

  return tropes

# files: analysis/trope_ll-female|male.json
def get_adjective_scores(tropes, male_trope_adj_ll, female_trope_adj_ll):
  '''
  Returns the adjectives associated with each trope. Takes a
  file list of tuples like so: [trope, [adjectives with ll scores...]]
  and converts it to a dictionary.
  Map looks like:

  trope -> [
    [ adj1, count, ll, normalized ll ],
    [ adj2, count, ll, normalized ll ]
  ]
  '''

  all_trope_adjs = male_trope_adj_ll + female_trope_adj_ll

  for trope_adjs in all_trope_adjs:
    trope = trope_adjs[0]
    adjectives = trope_adjs[1]
    tropes[trope]['adjectives'] = adjectives

  return tropes

# files: film_categories.json, trope_films-male|female.json
def get_occurance_over_time(tropes, male_trope_films, female_trope_films, categories):
  '''
  Gets occurance over time for a single trope. Returns map
  that looks like:

  trope -> [
    ['Films of the 1920s', count, %, count in decade ],
    ['Films of the 1930s', count, %, count in decade ]...
  ]
  '''

  decades_of_2000 = [
    'Films Of The 2000s-Franchises',
    'Films of 2000-2004',
    'Films of 2005-2009',
]

  tropes_dict = {}

  all_tropes = male_trope_films['values'] + female_trope_films['values']
  for trope in all_tropes:
    trope_id = trope['name']
    counts_over_time = trope['decade_counts']
    adjusted_counts_over_time = []

    for datum in counts_over_time:
      decade = datum[0]
      count = datum[1]
      # count_in_category = categories[decade]['tropes_'+gender+'_count']
      if decade != "Films of the 2000s":
        count_in_category = categories[decade]['film_count']
      else:
        count_in_category = categories[decades_of_2000[0]]['film_count'] + categories[decades_of_2000[1]]['film_count'] + categories[decades_of_2000[2]]['film_count']
      percentage = count / float(count_in_category) # relative count to total in category
      adjusted_counts_over_time.append((decade, count, percentage, count_in_category))

    tropes_dict[trope_id] = adjusted_counts_over_time

  for trope in tropes.values():
    if trope['id'] in tropes_dict:
      trope['occurrence_over_time'] = tropes_dict[trope['id']]

  return tropes

# Still need:
# trope -> appears in films





