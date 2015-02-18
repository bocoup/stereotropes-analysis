# Builds detail files for each film
#
# python -m src.film.detail --src=data/results/films_with_poster_files.json
# --dest=/Users/iros/dev/bocoup/tvtropes/data/films/detail
# --roles data/results/film_roles-female.json
# --roles data/results/film_roles-male.json
# --extended=True
#

from os.path import join
from src import util
from src.film import roles

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

def extract_detail_files(films, dest, roles, name=None, extended=False):

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

      if roles and data:
        # Extract role data
        data['roles'] = { 'm' : None, 'f' : None }
        if film['id'] in roles:
          data['roles'] = roles[film['id']]

        util.write_json(join(dest, data['id'] + '.json'), data)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--roles', help='Film role files for both genders', required=False, action='append')
    parser.add_argument('--dest', help='Destination folder', required=True)
    parser.add_argument('--extended', help='If true, will output extended form', required=False)
    parser.add_argument('--name', help='Specific movie to generate information on', required=False)

    args = parser.parse_args()

    films = util.read_json(args.src)

    movie_roles = None
    if args.roles:
      movie_roles = roles.get_roles(args.roles)

    extract_detail_files(films, args.dest, movie_roles, args.name, args.extended)
