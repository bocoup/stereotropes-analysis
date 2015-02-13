import requests
import json
import os

def write_json(path, data):
    output = open(path, 'w')
    output.write(json.dumps(data, indent=4))
    output.close

def read_json(path):
    file = open(os.path.abspath(path), 'r')
    data = json.load(file)
    file.close
    return data

def get_film_data(path):

  films = read_json(path)

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

data = get_film_data('data/results/films.json')
write_json('data/results/films_full.json', data)
