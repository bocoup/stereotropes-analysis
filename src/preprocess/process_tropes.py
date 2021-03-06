import tagger
import json
import os
from collections import OrderedDict
import trope_image_getter
import re
from src.film import similar

def write_json(path, data):
    output = open(path, 'w')
    output.write(json.dumps(data, indent=4))
    output.close

def read_json(path):
    file = open(os.path.abspath(path), 'r')
    data = json.load(file)
    file.close
    return data

def get_tropes_from_rdf(fp):
    trope_data = read_json(fp)
    results = list()
    for binding in trope_data['results']['bindings']:
        trope = binding['trope']['value'].split('/')[-1]
        # Not all the tropes currently have descriptions
        try:
            comment = binding['comment']['value']
            results.append((trope, comment))
        except:
            pass
    return results

def get_film_tropes_from_rdf(fp, blacklist):
    film_data = read_json(fp)
    blacklist = read_json(blacklist)

    series = list()
    for item in blacklist['results']['bindings']:
        series.append(item['series']['value'])

    results = list()
    for binding in film_data['results']['bindings']:
        try:
            trope = binding['trope']['value'].split('/')[-1]
            film = binding['film']['value'].split('/')[-1]
            film_name = binding['label']['value']
            # don't capture film category
            # film_category = binding['film_category_label']['value']
            role = binding['role']['value']
            if (binding['film']['value'] not in series):
                # Remove film category
                results.append((trope, film, film_name, role))
        except:
            pass

    return results


def tag_tropes(fp):
    tropes = read_json(fp)
    results = list()
    for tup in tropes:
        trope = tup[0]
        description = tup[1]
        result = tagger.tag(description)
        results.append((trope, result['tagged'], result['by_tag']))
    return results

def extract_adjectives(path, exclude):
    tagged_tropes = read_json(path)
    results = list()
    for tagged in tagged_tropes:
        try:
            adjectives = tagged[2]['JJ']
            adjectives = [a.lower() for a in adjectives]
        except:
            adjectives = []
        if exclude is not None:
            adjectives = [x for x in adjectives if x not in exclude]

        results.append((tagged[0], adjectives))
    return results


# find film name without the string
exp = re.compile('^[\w\s]+:\s(.*)')

# remove the year from the string, if it's there.
yr = re.compile(' (\d{4})|\(\d{4}\)')

def normalize_film_name(name):

    # remove the prefix
    film_name = exp.findall(name)
    parsed_name = ''
    if (len(film_name) > 0):
      parsed_name = film_name[0]
    else:
      parsed_name = name

    # remove whatever year mention
    m = yr.findall(parsed_name)
    if (len(m) > 0):
      no_year_name = re.subn(yr, '', parsed_name)[0]
    else:
      no_year_name = parsed_name

    return no_year_name

def build_film_tropes(film_trope_files):
    films = {}

    for fp in film_trope_files:
        gender = 'male'
        if 'female' in fp:
            gender = 'female'

        film_tropes = read_json(fp)

        for film in film_tropes:
            film_id = film[1]
            name = normalize_film_name(film[2])
            if film_id not in films:
                films[film_id] = {
                    'id' : film_id,
                    'name' : name,
                    'tropes': { 'male' : [], 'female' : [] }
                }
                films[film_id]['tropes'][gender] = [film[0]]
            else:
                if gender not in films[film_id]['tropes']:
                    films[film_id]['tropes'][gender] = []

                films[film_id]['tropes'][gender].append(film[0])

    return films

def extract_films(films, film_trope_files):

    films = read_json(films)
    film_tropes = build_film_tropes(film_trope_files)

    write_json("test.json", film_tropes)
    film_data = {}

    # Build film dictionary:
    for film in films['results']['bindings']:
        film_id = film['film']['value'].split('/')[-1]

        film_trope_list = { 'male' : [], 'female' : [] }

        if film_id in film_tropes:
            film_trope_list = film_tropes[film_id]['tropes']

        # don't add films if they have no tropes!
        if len(film_trope_list['male']) > 0 or len(film_trope_list['female']) > 0:

            film_name = normalize_film_name(film['label']['value'])
            film_category = film['film_category_label']['value']

            if film_id in film_data:
                # add category
                if film_category not in film_data[film_id]['categories']:
                    film_data[film_id]['categories'].append(film_category)
            else:
                # add entry for film
                film_data[film_id] = {
                    'id' : film_id,
                    'name' : film_name,
                    'categories': [film_category],
                    'tropes' : film_trope_list
                }

    return film_data.values()

def extract_film_tropes(path):
    film_roles = read_json(path)
    films = {
        'count': 0,
        'values': {}
    }

    for tup in film_roles:
        film = tup[2]
        if (film in films['values']):
            films['values'][film]['values'].append(tup[0]) # trope name
            films['values'][film]['count'] += 1
        else:
            films['values'][film] = {
                'name': film,
                'count': 1,
                'values' : [tup[0]]
            }


    return films['values'].values()

def extract_film_categories(path):
    films = read_json(path)
    categories = dict([])
    category_names = list()

    for film in films:
        for category in film['categories']:

            if category in categories:
                categories[category]['films'].append(film['id'])
                categories[category]['tropes']['female'] += film['tropes']['female']
                categories[category]['tropes']['male'] += film['tropes']['male']
                categories[category]['film_count'] += 1
                categories[category]['tropes_male_count'] += len(film['tropes']['male'])
                categories[category]['tropes_female_count'] += len(film['tropes']['female'])
            else:
                categories[category] = {
                    'films' : [film['id']],
                    'category' : category,
                    'tropes' : {
                        'male' : film['tropes']['male'],
                        'female' : film['tropes']['female'],
                    },
                    'film_count' : 1,
                    'tropes_male_count' : len(film['tropes']['male']),
                    'tropes_female_count' : len(film['tropes']['female'])
                }

    return categories

def build_trope_count_per_decade(tropes):
    decades = [
        'Films of the 1920s',
        'Films of the 1930s',
        'Films of the 1940s',
        'Films of the 1950s',
        'Films of the 1960s',
        'Films of the 1970s',
        'Films of the 1980s',
        'Films of the 1990s',
        'Films of the 2000s',
        'Films Of The 2000s-Franchises',
        'Films of 2000-2004',
        'Films of 2005-2009',
        'Films of the 2010s'
    ]

    decades_of_2000 = [
        'Films Of The 2000s-Franchises',
        'Films of 2000-2004',
        'Films of 2005-2009',
    ]

    for trope_name in tropes['values']:
        decade_counts = {}
        trope = tropes['values'][trope_name]

        # count the decade occurace
        for film_category in trope['categories']:
            if film_category in decades:
                if film_category in decade_counts:
                    decade_counts[film_category] += 1
                else:
                    decade_counts[film_category] = 1

        # fill in gaps with zeroes for decades that
        # were not mentioned and convert the whole
        # thing to an ordered list.
        decade_counts_list = list()
        for decade in decades:
            if decade not in decade_counts:
                decade_counts[decade] = 0

            if decade in decades_of_2000:
                decade_counts['Films of the 2000s'] += decade_counts[decade]
                del decade_counts[decade]



        min_max = [float("inf"), 0]
        for decade in decades:
            if decade not in decades_of_2000:
                decade_counts_list.append((decade, decade_counts[decade], trope_name))

                # assemble biggest diff between values
                if (decade_counts[decade] < min_max[0]):
                    min_max[0] = decade_counts[decade]
                if (decade_counts[decade] > min_max[1]):
                    min_max[1] = decade_counts[decade]

        tropes['values'][trope_name]['decade_counts_diff'] = min_max[1] - min_max[0]
        tropes['values'][trope_name]['decade_counts'] = decade_counts_list

    return tropes

def compute_film_similarity(films):
    films = read_json(films)
    return similar.get_similiar_films(films)

def extract_trope_films(films, film_roles):

    # build film dictionary
    films = read_json(films)
    films_dict = {}
    for film in films:
        films_dict[film['id']] = film

    film_roles = read_json(film_roles)

    tropes = {
        'count' : 0,
        'values' : {}
    }

    for role in film_roles:
        trope = role[0]
        film_id = role[1]

        # Not all films were found, so we aren't going to count the roles
        # for those films.
        if film_id in films_dict:
            if (trope in tropes['values']):

                # Aggregate trope -> film appearance + counts/unique

                if (film_id not in tropes['values'][trope]['films']):
                    tropes['values'][trope]['films_unique'] += 1

                tropes['values'][trope]['films'].append(film_id)
                tropes['values'][trope]['films_count'] += 1

            else:
                tropes['count'] += 1

                tropes['values'][trope] = {
                    'name' : trope,
                    'films' : [film_id],
                    'films_count' : 1,
                    'films_unique' : 1,
                    'categories': [],
                    'categories_count': 0,
                    'categories_unique': 0
                }

            # Aggregate trope -> film category appearance + counts/unique
            film_categories = films_dict[film_id]['categories']
            for cat in film_categories:
                if (cat not in tropes['values'][trope]['categories']):
                    tropes['values'][trope]['categories_unique'] += 1

            tropes['values'][trope]['categories'] += film_categories
            tropes['values'][trope]['categories_count'] += len(film_categories)

    tropes = build_trope_count_per_decade(tropes)
    tropes['values'] = tropes['values'].values()
    return tropes

# This will combine the words (adjectives) from each corpus file in corpora
# into one flat list.
def make_base_corpus(corpora):
    results = list()
    for corpus_fp in corpora:
        adjectives = read_json(corpus_fp)
        for tup in adjectives:
            results.append(tup[1])
    #flatten data at the end
    return sum(results, [])


# This will remove tropes found in the file provided in the second parameter
# from the file provided from the first and return that as a new collection.
def filter_tropes(target, other):
    target_tropes = read_json(target)
    other_tropes = read_json(other)

    other_trope_names = [t[0] for t in other_tropes]
    result = [t for t in target_tropes if t[0] not in other_trope_names]
    return result


def get_images(trope_list, destination_folder):
    results = trope_image_getter.get_images(sorted(trope_list), destination_folder)
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process Tropes')

    parser.add_argument('--source', nargs='+', help='source file', required=True)
    parser.add_argument('--dest', help='source file', required=True)
    parser.add_argument('--command', help='command to run', required=True)
    parser.add_argument('--label', required=False)
    parser.add_argument('--exclude_adjectives', help='path to file with adjectives to exclude', required=False, default=None)

    args = parser.parse_args()

    if args.command == 'extract_tropes':
        tropes = get_tropes_from_rdf(args.source[0])
        write_json(args.dest, tropes)
    elif args.command == 'extract_film_trope_tuples':
        films = get_film_tropes_from_rdf(args.source[0], args.source[1])
        write_json(args.dest, films)
    elif args.command == 'extract_films':
        films = extract_films(args.source[0], [args.source[1], args.source[2]])
        write_json(args.dest, films)
    elif args.command == 'extract_film_categories':
        film_categories = extract_film_categories(args.source[0])
        write_json(args.dest, film_categories)
    elif args.command == 'extract_film_tropes':
        film_tropes = extract_film_tropes(args.source[0])
        write_json(args.dest, film_tropes)
    elif args.command == 'extract_trope_films':
        trope_film_categories = extract_trope_films(args.source[0],args.source[1])
        write_json(args.dest, trope_film_categories)
    elif args.command == 'find_similar_films':
        films_with_similar_films = compute_film_similarity(args.source[0])
        write_json(args.dest, films_with_similar_films)
    elif args.command == 'tag_tropes':
        tagged_results = tag_tropes(args.source[0])
        write_json(args.dest, tagged_results)
    elif args.command == 'extract_adjectives':
        if args.exclude_adjectives is not None:
            exclude = read_json(args.exclude_adjectives)

        adjectives = extract_adjectives(args.source[0], exclude)
        write_json(args.dest, adjectives)
    elif args.command == 'make_base_corpus':
        corpus = make_base_corpus(args.source)
        write_json(args.dest, corpus)
    elif args.command == 'filter_tropes':
        filtered = filter_tropes(args.source[0], args.source[1])
        write_json(args.dest, filtered)
    elif args.command == 'get_images':
        trope_info = read_json(args.source[0])
        trope_list = [t[0] for t in trope_info]
        res = get_images(trope_list, args.dest)
        write_json(os.path.join(args.dest, 'results.json'), res)
    else:
        print('Unknown Command')


