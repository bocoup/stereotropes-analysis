from os.path import splitext, basename, join, isfile

def get_poster_path(film_id, image_url, dest_folder):
    extension = splitext(basename(image_url))[1]
    path = join(dest_folder, film_id + extension)
    return path

def does_poster_exist(film_id, image_url, dest_folder):
    path = get_poster_path(film_id, image_url, dest_folder)
    return isfile(path)

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
    base['similar'] = film['similar']

    return base
  else:
    return None