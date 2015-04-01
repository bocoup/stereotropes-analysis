import os
from os.path import join
from os.path import dirname
from src import util
import re
import math

def parse_input(filename):
    '''
    Read in the json starting file
    '''
    return util.read_json(args.src)

def write_output(films, filename):
    '''
    Write out the list of files in a json format.
    '''
    util.write_json(filename, films)

def score(film):
    '''
    returns the rating score for a film
    right now based on rotten tomatoes scores
    a film only has a score if it has both audience_score and
    a critics_score. The score is the audience_score.
    '''
    if "#" in film["id"]:
        return 0
    if ("rtmetadata" in film and "ratings" in film["rtmetadata"] and "audience_score" in film["rtmetadata"]["ratings"]) and ( "critics_score" in film["rtmetadata"]["ratings"] and film["rtmetadata"]["ratings"]["critics_score"] > 0):
        return film["rtmetadata"]["ratings"]["audience_score"]
    return 0

def get_top(all_films, top_n):
    '''
    Given a list of films, this pulls out the top_n
    where films are sorted by their score (rating)
    '''
    sorted_films = sorted(all_films, key=lambda film: score(film), reverse = True)

    return sorted_films[0:top_n + 1]

def genres(film):
    '''
    Returns a list of genres for a given film
    '''
    if ("metadata" in film and "Genre" in film["metadata"]):
        return [g.strip().lower().replace("/","_") for g in film["metadata"]["Genre"].split(",")]
    return []

def decade_of(year):
    return "{}s".format(int(math.floor(float(year) / 10.0) * 10))

def decades(film):
    '''
    Returns a list of decades for a given film
    There will be only one decade - but returned as
    a list to make the processing work the same as
    genres
    '''

    # sometimes this is an int. other times its an empty string :(
    if ("rtmetadata" in film and "year" in film["rtmetadata"] and (not isinstance(film["rtmetadata"]["year"], basestring))):
        year = film["rtmetadata"]["year"]
        return [decade_of(year)]
    elif ("metadata" in film and "Year" in film["metadata"] and len(film["metadata"]["Year"]) > 0):
        # sometimes this has a weird unicode dash in it that needs to be purged.
        year = re.split("\D",film["metadata"]["Year"])[0]
        year = int(year.strip())
        return [decade_of(year)]
    return []

def split_genres(all_films):
    '''
    returns a dict of genres where the value
    of each is a list of films in that genre
    '''
    all_genres = {}
    for film in all_films:
        film_genres = genres(film)
        for genre in film_genres:
            if not genre in all_genres:
                all_genres[genre] = []
            all_genres[genre].append(film)

    return all_genres

def split_decades(all_films):
    '''
    returns a dict of decades where the value
    of each is a list of films in that decade
    '''
    all_decades = {}
    for film in all_films:
        film_decades = decades(film)
        for decade in film_decades:
            if not decade in all_decades:
                all_decades[decade] = []
            all_decades[decade].append(film)

    return all_decades

def get_fields(films):
    '''
    Given a set of films, return a list
    of the same films - but with just the
    attributes we care about (name, id, poster_url)
    '''

    # we want to keep the names as consistent as possible with
    # the films info files - so we need to remap poster_filename
    attrs = {"name":"name", "id":"id", "poster_filename":"poster_url"}

    output = []
    for film in films:
        data = {attrs[k]: film[k] for k in attrs.keys() if (k in film)}
        output.append(data)

    return output

def write_top(film_sets, top_n, dest_dir):
    for film_set in film_sets.keys():
        top_films = get_top(film_sets[film_set], top_n)
        out_filename = "{}/{}_top_{}.json".format(dest_dir, film_set, top_n)
        print out_filename
        output = get_fields(top_films)
        write_output(output, out_filename)
    return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--dest', help='Destination file', required=True)
    parser.add_argument('--top', help='Only output top N rotten tomatoes scored films', required=False)
    parser.add_argument('--genres', help='Split up Genres for Top N', required=False)
    parser.add_argument('--decades', help='Output decades for Top N', required=False)

    args = parser.parse_args()
    films = parse_input(args.src)


    # set default top_n for genres and decades output
    top_n = 100
    if args.top:
        top_n = int(args.top)
    dest_dir = dirname(args.dest)

    if args.genres:
        genres = split_genres(films)
        write_top(genres, top_n, dest_dir)
        out_filename = "{}/genres.json".format(dirname(args.dest))
        write_output(genres.keys(),out_filename)

    elif args.decades:
        decades = split_decades(films)
        write_top(decades, top_n, dest_dir)
        out_filename = "{}/decades.json".format(dirname(args.dest))
        write_output(decades.keys(),out_filename)
    elif args.top:
        films = get_top(films, int(args.top))
        output = get_fields(films)
        write_output(output, args.dest)
    else:
        output = get_fields(films)
        write_output(output, args.dest)

