# Scrapes OMDB for movie metadata
#
# python -m src.film.omdb --dest=data/results/films_full.json --src=data/results/films.json
import requests
import json
from src import util

def scrape(path):

  films = util.read_json(path)

  for film in films:

    try:
      film['name'] = film['name'].replace('"', '')
      url = 'http://www.omdbapi.com/?t=' + film['name'] + '&y=&plot=full&r=json'

      print "Scraping " + url

      r = requests.get(url)
      response = json.loads(r.text)

      if 'Title' in response:
        # Film data found!
        film['metadata'] = response
        print response['Title']
      else:
        film['metadata'] = None

    except:
      pass

  return films

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Scrape OMDB for movie data')
    parser.add_argument('--src', help='Source films', required=True)
    parser.add_argument('--dest', help='Destination for film dictionary', required=False)

    args = parser.parse_args()

    data = scrape(args.src)
    util.write_json(args.dest, data)
