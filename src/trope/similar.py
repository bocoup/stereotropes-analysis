from src import util
from src.film import util as filmutil
from collections import Counter
from itertools import groupby

def get_film_tropes(film):
  tropes = []
  if 'female' in film['tropes']:
    tropes += film['tropes']['female']
  if 'male' in film['tropes']:
    tropes += film['tropes']['male']

  return tropes

def get_similar_tropes(tropes, films):

  edge_list = []
  movie_list = {}
  for film in films:
    trope_list = get_film_tropes(film)
    shared = list(set(trope_list))
    if len(shared) > 0:
      for idx, t1 in enumerate(shared):
        for i in range(idx+1, len(shared)-1):
          t2 = shared[i]
          if t1 != t2:
            sorted_tropes = sorted([t1, t2])
            pair = tuple(sorted_tropes)
            edge_list.append(pair)

            if pair in movie_list:
              movie_list[pair].append(film['id'])
            else:
              movie_list[pair] = [film['id']]

  # add them up:
  links = []
  counter = Counter(edge_list)
  for item in counter:
    links.append({
      'trope' : item[0],
      'related_trope' : item[1],
      'count' : counter[item],
      'films' : movie_list[tuple(sorted([item[0], item[1]]))]
    })

  # group by trope:
  for trope, group in groupby(links, lambda t: t['trope']):
    if trope in tropes:
      if 'similar' not in tropes[trope]:
        tropes[trope]['similar'] = list(group)
      else:
        tropes[trope]['similar'].append(list(group)[0])

  # reduce to top N
  for trope in tropes.values():
    if 'similar' in trope:
      trope['similar'].sort(key=lambda t: -t['count'])
      trope['similar'] = trope['similar'][1:10]

  return tropes


