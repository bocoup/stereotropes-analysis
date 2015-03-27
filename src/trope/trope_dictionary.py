from src import util
import re

def to_name(trope_id):
    '''Return the display name for a trope id'''
    if(trope_id == 'GENTLEMANADVENTURER'):
        return 'Gentleman Adventurer'
    else:
        return re.sub('([a-z])([A-Z])','\g<1> \g<2>', trope_id)

def image_url(id, url):
    if url:
        extension = url.split('.')[-1]
        return 'assets/data/tropes/images/' + id + '.' + extension
    else:
        return None

def adjectives(trope):
    return trope['adjs'][0:5]

def map_array(trope_array, attr_name):
    """Convert array of arrays into dict
    """
    return {trope[0]: {attr_name: trope[1]} for trope in trope_array}

def basic_info(tropes):
    """Return a dict of base trope info

    Format will be the following
        tropeId -> {
            id:
            name:
            gender:
            adjs:
            image_url:
        }
    """
    info = extended_info(tropes)

    for k, v in info.iteritems():
        del v['description']
    return info

def extended_info(tropes):
    """Return a dict of extended trope info.

    Format will be the following
        tropeId -> {
            id:
            name:
            description:
            gender:
            adjs:
            image_url:
        }
    """
    results = dict()
    for k, v in tropes.iteritems():
        results[k] = {
            'id': k,
            'name': to_name(k),
            'description': v['desc'],
            'gender': v['gender'],
            'image_url': image_url(k, v['img']),
            'adjs' : adjectives(v)
        }
    return results

def build_tropes():
    files = {
        'data/results/images/male/results.json' : {'type':'img', 'gender':'m'},
        'data/results/images/female/results.json' : {'type':'img', 'gender':'f'},
        'data/results/only_tropes-male.json' : {'type':'desc', 'gender':'m'},
        'data/results/only_tropes-female.json' : {'type':'desc', 'gender':'f'},
        'data/results/tropes_adjectives-female.json' : {'type':'adjs', 'gender':'f'},
        'data/results/tropes_adjectives-male.json' : {'type':'adjs', 'gender':'m'}
        }

    all_tropes = {}
    for filename, options in files.iteritems():
        attr_type = options['type']
        data = util.read_json(filename)
        attrs = map_array(data, attr_type)
        for k, v in attrs.iteritems():
            if(k not in all_tropes):
                all_tropes[k] = {}
            all_tropes[k].update(v)
            if('gender' not in v):
                all_tropes[k]['gender'] = options['gender']
            elif(v['gender'] != options['gender']):
                print "ERROR: genders don't match"

    return all_tropes

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--dest', help='source file', required=True)
    parser.add_argument('--filter', required=False)
    parser.add_argument('--extended', required=False, action='store_true')

    args = parser.parse_args()
    all_tropes = build_tropes()

    if args.filter:
        filter_list = util.read_json(args.filter)
        all_tropes = {k:v for (k,v) in all_tropes.iteritems() if k in filter_list}

    if args.extended:
        res = extended_info(all_tropes)
        util.write_json(args.dest, res)
    else:
        res = basic_info(all_tropes)
        util.write_json(args.dest, res)
