import os
from os.path import join
from os.path import dirname
from src import util

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

def get_fields(films):
    '''
    Given a set of films, return a list
    of the same films - but with just the
    attributes we care about (name and id)
    '''
    attrs = ["name", "id"]

    output = []
    for film in films:
        data = {k: film[k] for k in attrs}
        output.append(data)

    return output

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--dest', help='Destination file', required=True)
    parser.add_argument('--top', help='Only output top N rotten tomatoes scored films', required=False)
    parser.add_argument('--genres', help='Split up Genres for Top N', required=False)

    args = parser.parse_args()
    films = parse_input(args.src)
    if args.genres:
        genres = split_genres(films)
        for genre in genres.keys():
            top_n = 100
            if args.top:
                top_n = int(args.top)
            top_films = get_top(genres[genre], top_n)
            out_filename = "{}/{}_top_{}.json".format(dirname(args.dest), genre, top_n)
            print out_filename
            output = get_fields(top_films)
            write_output(output, out_filename)

    elif args.top:
        films = get_top(films, int(args.top))
        output = get_fields(films)
        write_output(output, args.dest)
    else:
        output = get_fields(films)
        write_output(output, args.dest)

