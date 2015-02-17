from os.path import splitext, basename, join, isfile

def get_poster_path(film_id, image_url, dest_folder):
    extension = splitext(basename(image_url))[1]
    path = join(dest_folder, film_id + extension)
    return path

def does_poster_exist(film_id, image_url, dest_folder):
    path = get_poster_path(film_id, image_url, dest_folder)
    return isfile(path)