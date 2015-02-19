from src import util
from src.film import util as filmutil


def get_film_tropes(film):
  tropes = []
  if 'female' in film['tropes']:
    tropes += film['tropes']['female']
  if 'male' in film['tropes']:
    tropes += film['tropes']['male']

  return tropes

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def get_similiar_films(films):

  for film in films:
    tropes = get_film_tropes(film)

    similiar_films = []

    for other_film in films:
      if film['id'] != other_film['id']:
        other_tropes = get_film_tropes(other_film)

        shared = intersect(tropes, other_tropes)

        if len(shared) > 0:
          similiar_films.append((other_film, shared, len(shared)))


    sorted_similiar_films = sorted(similiar_films, key=lambda tup: -tup[2])[0:5]
    similar_list = []

    for tup in sorted_similiar_films:
      film_data = filmutil.get_film_base(tup[0])
      film_data['shared'] = tup[1]
      film_data['shared_count'] = tup[2]
      similar_list.append(film_data)

    film['similar'] = similar_list

  return films


