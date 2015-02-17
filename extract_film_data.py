import tagger
import json
import os
from collections import OrderedDict
import re

def write_json(path, data):
    output = open(path, 'w')
    output.write(json.dumps(data, indent=4))
    output.close

def read_json(path):
    file = open(os.path.abspath(path), 'r')
    data = json.load(file)
    file.close
    return data

def find_film(name, filmfile):
  films = read_json('data/results/films.json')

  for film in films:
    if (film['name'] == name):
      return film

  return None

# trope_ll_file - [trope name, [[adj1], [adj2]...]]
# adjective_ll_file - [[adj1], [adj2], ...]
# tropes - [trope1, trope2, trope3]

def build_trope_adjectives(trope_ll_file, adjective_ll_file, tropes, output_tropes, output_adj):
  tropes_ll = read_json(trope_ll_file)
  adjective_ll = read_json(adjective_ll_file)

  # build map from tropes_ll for quicker lookup
  tropemap = {}
  for trope_ll in tropes_ll:
    tropemap[trope_ll[0]] = trope_ll[1]

  # build map from adjectives_ll for quicker lookup - these are not trope
  # specific, just gender specific.
  adjective_map = {}
  for adj in adjective_ll:
    adjective_map[adj[0]] = adj

  adjective_subset = {}
  trope_adjectives_subset = {}
  for trope in tropes:

    # Find the trope with the data
    trope_adjectives = tropemap[trope]

    if trope_adjectives:
      for trope_adjective in trope_adjectives:
        adj = trope_adjective[0]

        # find adjective metadata in global dict
        adj_data = adjective_map[adj]

        # store the adjective data in our subset
        if (adj_data):
          if adj not in adjective_subset:
            adjective_subset[adj] = adj_data

        if trope not in trope_adjectives_subset:
          trope_adjectives_subset[trope] = [trope, [adj_data[0]]]
        else:
          print trope_adjectives_subset[trope]
          trope_adjectives_subset[trope][1].append(adj_data[0])

  write_json(output_adj, adjective_map.values())
  write_json(output_tropes, trope_adjectives_subset.values())

film = find_film("Frozen", "data/results/films.json")

build_trope_adjectives("data/analysis/trope_ll-male.json",
  "data/analysis/ll-male.json",
  film["tropes"]["male"],
  "data/film/trope_ll-male.json",
  "data/film/ll-male.json",
)

build_trope_adjectives("data/analysis/trope_ll-female.json",
  "data/analysis/ll-female.json",
  film["tropes"]["female"],
  "data/film/trope_ll-female.json",
  "data/film/ll-female.json",
)
