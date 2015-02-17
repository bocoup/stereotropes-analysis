import requests
import requests_cache
from os.path import splitext, basename, join
import time
import json
import math
import wget
from src import util
from src.film import util as filmutil

def get_film_base(film):
  base = {
    'id' : film['id'],
    'name' : film['name']
  }
  if 'poster_filename' in film:
    base['poster_url'] = film['poster_filename']

  return base

def get_film_extendeed(film):
  base = get_film_base(film)
  if 'metadata' in film and film['metadata'] is not None:
    base['plot'] = film['metadata']['Plot']
    base['release_year'] = film['metadata']['Year']
    base['genres'] = film['metadata']['Genre']
    base['imdbid'] = film['metadata']['imdbID']

    return base
  else:
    return None

def extract_detail_files(films, dest, name=None, extended=False):

  for film in films:
    write = True
    if name is not None and film['name'] != name:
        write = False

    if write:
      data = None
      if extended:
        data = get_film_extendeed(film)
      else:
        data = get_film_base(film)

      if data:
        print data['name']
        util.write_json(join(dest, data['id'] + '.json'), data)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--dest', help='Destination folder', required=True)
    parser.add_argument('--extended', help='If true, will output extended form', required=False)
    parser.add_argument('--name', help='Specific movie to generate information on', required=False)

    args = parser.parse_args()

    films = util.read_json(args.src)

    extract_detail_files(films, args.dest, args.name, args.extended)
