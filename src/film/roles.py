from src import util
import tagger

def get_roles(trope_files):
  ''' Returns the male and female roles identified in this movie'''

  movie_tropes = {}
  movie_trope_dictionary = {}

  for trope_file in trope_files:

    tropes = util.read_json(trope_file)

    # determine gender based on trope.
    gender = 'm'
    if 'female' in trope_file:
      gender = 'f'

    print "Processing " + gender

    # build map:
    # movieId -> [trope1, trope2, trope3]
    for idx, tup in enumerate(tropes):
      if idx % 100 == 0:
        print str(idx) + " out of " + str(len(tropes))

      trope = tup[0]
      film_id = tup[1]
      role = tup[3]

      if film_id not in movie_tropes:
        movie_tropes[film_id] = {}
        movie_trope_dictionary[film_id] = {}

      if gender not in movie_tropes[film_id]:
        movie_tropes[film_id][gender] = []
        movie_trope_dictionary[film_id][gender] = {}

      if (
          # if we haven't seen this trope appear yet for this film
          trope not in movie_trope_dictionary[film_id][gender] or

          # or, we've seen this trope but the description is different
          (
            trope in  movie_trope_dictionary[film_id][gender] and
            role not in movie_trope_dictionary[film_id][gender][trope]
          )
        ):
        tags = tagger.tag(role)
        adjectives = []
        if 'JJ' in tags['by_tag']:
          adjectives = tags['by_tag']['JJ']

        movie_tropes[film_id][gender].append({
          'id' : trope,
          'role' : role,
          'adjectives' : adjectives
        })

        if trope in movie_trope_dictionary[film_id][gender]:
          movie_trope_dictionary[film_id][gender][trope].append(role)
        else:
          movie_trope_dictionary[film_id][gender][trope] = [role]

  return movie_tropes