# Builds detail files for each film
#
# python -m src.film.detail --src=data/results/films_with_posters_and_similiar_films.json
# --dest=/Users/iros/dev/bocoup/tvtropes/data/films/detail
# --roles data/results/film_roles-female.json
# --roles data/results/film_roles-male.json
# --extended=True
#

from os.path import join
from src import util
from src.film import roles
from src.film import util as filmutil

def write_detail_files(film_details, dest):
  '''
  Write out the details of all films to a dest folder
  '''

  for film in film_details.values():
    util.write_json(join(dest, film['id'] + '.json'), film)

def get_roles(films, roles):
  '''
  Add film roles to films
  '''

  for film in films.values():
    film['roles'] = { 'm' : None, 'f' : None }
    if film['id'] in roles:
      film['roles'] = roles[film['id']]

  return films

def get_details(films, name=None, extended=False):
  '''
  Assemble film dictionary with details, either extended or
  the base details
  '''

  film_details = {}

  for film in films:
    write = True
    if name is not None and film['name'] != name:
        write = False

    if write:
      data = None
      if extended:
        data = filmutil.get_film_extendeed(film)
      else:
        data = filmutil.get_film_base(film)

      if data:
        film_details[data['id']] = data

  return film_details


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
    film_details = get_details(films, args.name, args.extended)

    movie_roles = None
    film_roles = film_details
    if args.roles:
      movie_roles = roles.get_roles(args.roles)
      film_roles = get_roles(film_details, movie_roles)

    write_detail_files(film_roles, args.dest)
