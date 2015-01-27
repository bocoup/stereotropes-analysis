import tagger
import json
import os
from collections import OrderedDict

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

def get_film_from_rdf(fp):
    film_data = read_json(fp)
    results = list()
    for binding in film_data['results']['bindings']:
        try:
            trope = binding['trope']['value'].split('/')[-1]
            film = binding['film']['value'].split('/')[-1]
            film_name = binding['label']['value']
            film_category = binding['film_category_label']['value']

            results.append((trope, film, film_name, film_category))
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

def extract_adjectives(path):
    tagged_tropes = read_json(path)
    results = list()
    for tagged in tagged_tropes:
        # print tagged[2][u'JJ']
        try:
            adjectives = tagged[2]['JJ']
        except:
            adjectives = []
        results.append((tagged[0], adjectives))
    return results

def extract_film_categories(path):
    film_roles = read_json(path)
    categories = dict([])
    category_names = list()

    for tup in film_roles:
        film_category = tup[-1]
        if (film_category in categories):
            categories[film_category].append((tup[0], tup[1]))
        else:
            categories[film_category] = [(tup[0], tup[1])]
            category_names.append(film_category)

    for cat in category_names:
        tuples = categories[cat]
        categories[cat] = {
            'count' : len(tuples),
            'films' : [tup[1] for tup in tuples],
            'tropes': [tup[0] for tup in tuples]
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
                decade_counts_list.append((decade, decade_counts[decade]))

                # assemble biggest diff between values
                if (decade_counts[decade] < min_max[0]):
                    min_max[0] = decade_counts[decade]
                if (decade_counts[decade] > min_max[1]):
                    min_max[1] = decade_counts[decade]

        tropes['values'][trope_name]['decade_counts_diff'] = min_max[1] - min_max[0]
        tropes['values'][trope_name]['decade_counts'] = decade_counts_list

    return tropes


def extract_trope_films(path):
    film_roles = read_json(path)
    tropes = {
        'count' : 0,
        'values' : {}
    }
    for tup in film_roles:
        trope = tup[0]
        if (trope in tropes['values']):

            # Aggregate trope -> film appearance + counts/unique

            if (tup[1] not in tropes['values'][trope]['films']):
                tropes['values'][trope]['films_unique'] += 1

            tropes['values'][trope]['films'].append(tup[1])
            tropes['values'][trope]['films_count'] += 1

            # Aggregate trope -> film category appearance + counts/unique

            if (tup[3] not in tropes['values'][trope]['categories']):
                 tropes['values'][trope]['categories_unique'] += 1

            tropes['values'][trope]['categories'].append(tup[3])
            tropes['values'][trope]['categories_count'] += 1

        else:
            tropes['count'] += 1

            tropes['values'][trope] = {
                'name' : trope,
                'films' : [tup[1]],
                'films_count' : 1,
                'films_unique' : 1,
                'categories': [tup[3]],
                'categories_count': 1,
                'categories_unique': 1
            }

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


if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Process Tropes')

    parser.add_argument('--source', nargs='+', help='source file', required=True)
    parser.add_argument('--dest', help='source file', required=True)
    parser.add_argument('--command', help='command to run', required=True)

    args = parser.parse_args()

    if args.command == 'extract_tropes':
        tropes = get_tropes_from_rdf(args.source[0])
        write_json(args.dest, tropes)
    elif args.command == 'extract_films':
        films = get_film_from_rdf(args.source[0])
        write_json(args.dest, films)
    elif args.command == 'extract_film_categories':
        film_categories = extract_film_categories(args.source[0])
        write_json(args.dest, film_categories)
    elif args.command == 'extract_trope_films':
        trope_film_categories = extract_trope_films(args.source[0])
        write_json(args.dest, trope_film_categories)
    elif args.command == 'tag_tropes':
        tagged_results = tag_tropes(args.source[0])
        write_json(args.dest, tagged_results)
    elif args.command == 'extract_adjectives':
        adjectives = extract_adjectives(args.source[0])
        write_json(args.dest, adjectives)
    elif args.command == 'make_base_corpus':
        corpus = make_base_corpus(args.source)
        write_json(args.dest, corpus)
    elif args.command == 'filter_tropes':
        filtered = filter_tropes(args.source[0], args.source[1])
        write_json(args.dest, filtered)
    else:
        print('Unknown Command')


