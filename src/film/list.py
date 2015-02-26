from os.path import join
from src import util

def parse_input(filename):
    '''
    Read in the data
    '''
    return util.read_json(args.src)

def write_output(films, filename):
    '''
    Write out the list of files
    '''
    util.write_json(filename, films)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--src', help='Source films dictionary', required=True)
    parser.add_argument('--dest', help='Destination folder', required=True)

    args = parser.parse_args()
    films = parse_input(args.src)
    attrs = ["name", "id"]

    output = []
    for film in films:
        data = {k: film[k] for k in attrs}
        output.append(data)

    write_output(output, args.dest)

