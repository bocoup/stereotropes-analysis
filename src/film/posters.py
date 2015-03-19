# A module to download film posters from rotten tomatoes
# You can:
#  - Scrape rotten tomatoes for metadata and get movie posters
#  - Download poster images
#
# You don't have to do both. For example, this will scrape the data:
# python -m src.film.posters --src=data/results/films_full.json
#   --dest=data/results/ft.json --scrape=True --failed=data/results/ft_f.json
#
# And this will scrape AND download it:
# python -m src.film.posters --src=data/results/films_full.json
#   --dest=data/results/ft.json --scrape=True --failed=data/results/ft_f.json
#   --poster_dest=test/
#
# If the data is already scraped, you can set scrape=False and then load the
# file source with the rotten tomato information in src and provide a poster
# destination directory.

import requests
import requests_cache
from os.path import splitext, basename, join
import time
import json
import math
import wget
from src import util
from src.film import util as filmutil

requests_cache.install_cache('rotten_tomatoes_web_cache')

apiKeys = util.read_json('src/film/api-keys.json')

def rotten_tomato_url(film):
    """Returns a rotten tomato data url for a specific movie."""

    return ('http://api.rottentomatoes.com/api/public/v1.0/movies.json?'
            'q=' + '+'.join(film['name'].split(' ')) + '&page_limit=10&page=1'
            '&apikey=' + apiKeys['rotten-tomatoes'])

def normalize_poster_url(movie):
    image_url = movie['posters']['thumbnail']

    if 'tmb' in movie['posters']['thumbnail']:
        image_url = movie['posters']['thumbnail'].replace('tmb', '320')
    elif 'unsafe' in movie['posters']['thumbnail']:
        dimensions_str = movie['posters']['thumbnail'].split("/")[4]
        dimensions = dimensions_str.split("x")
        ratio = int(dimensions[0]) / float(dimensions[1])
        new_dimensions = [320, int(math.floor(320 / ratio))]
        image_url = movie['posters']['thumbnail'].replace(dimensions_str, str(new_dimensions[0])+"x"+str(new_dimensions[1]))

    if 'poster_default_thumb' in image_url:
        return None
    else:
        return image_url

def find_movie(imdbid, movies):
    for movie in movies:
        if 'alternate_ids' in movie:
            if (movie['alternate_ids']['imdb'] == imdbid):
                return movie
    return None

def get_all_posters(films, sleep_interval=0.5):
    failed_films = []
    for film in films:
        if 'rtmetadata' not in film:
            res = get_poster(film)
            # returned structure:
            # (film, poster_url, movie, True) > if found True, False if not.

            if res[3] == True:

                # Save poster
                if res[1] is not None:
                    film['poster'] = res[1]

                # Save rotten tomatoes metadata in case we want something from it
                if res[2] is not None:
                    film['rtmetadata'] = res[2]
            else:
                failed_films.append(film)

            time.sleep(sleep_interval)

    return [films, failed_films]

def get_poster(film):
    url = rotten_tomato_url(film)

    try:
        r = requests.get(url)
        response = json.loads(r.text)

        poster_url = None
        if (response['total'] > 0):

            if film['metadata'] is not None:
                imdbid = film['metadata']['imdbID'][2:]

                # Find the right movie match from rotten tomatoes based on the
                # id that we have from imdb (collected from omdb.)
                movie = find_movie(imdbid, response['movies'])
                if movie is not None:
                    poster_url = normalize_poster_url(movie)

        return (film, poster_url, movie, True)
    except:
        return (film, None, None, False)

def download_poster_images(films, dest_folder, sleep_interval=0.5):
    failed_films = []

    for film in films:
        poster_url = None
        if 'poster' in film:

            poster_url = film['poster']
            poster_file_path = filmutil.get_poster_path(film['id'], poster_url, dest_folder)

            if not filmutil.does_poster_exist(film['id'], poster_url, dest_folder):
                try:
                    print poster_url
                    wget.download(poster_url, out=poster_file_path)
                    time.sleep(sleep_interval)
                except:
                    failed_films.append(film)

            film['poster_filename'] = basename(poster_file_path)

    return films

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--dest', help='Destination for film dictionary', required=False)
    parser.add_argument('--failed', help='Where to write failing films', required=False)
    parser.add_argument('--scrape', dest='scrape', action='store_true')
    parser.add_argument('--no-scrape', dest='scrape', action='store_false')
    parser.add_argument('--poster_dest', help='Destination dir for film posters', required=False)

    args = parser.parse_args()

    films_with_posters = None

    # Download rotten tomato data:
    if args.scrape:
        films = util.read_json(args.src)
        films_with_posters = get_all_posters(films)
        util.write_json(args.dest, films_with_posters[0])
        if args.failed:
            util.write_json(args.failed, films_with_posters[1])

    # Download posters
    if args.poster_dest:
        if args.scrape:
            films = films_with_posters[0]
        else:
            films = util.read_json(args.src)

        # download poster images
        films_with_poster_files = download_poster_images(films, args.poster_dest)

        # write out the updated dest file.
        util.write_json(args.dest, films_with_poster_files)
