import util
import re

def to_name(trope_id):
    '''Return the display name for a trope id'''
    if(trope_id == 'GENTLEMANADVENTURER'):
        return 'Gentleman Adventurer'
    else:
        return re.sub('([a-z])([A-Z])','\g<1> \g<2>', trope_id)

def image_url(id, url):
    if url:
        return 'assets/data/tropes/images/' + id + '.jpg'
    else:
        return None


def basic_info(male_trope_info, male_image_info, female_trope_info, female_image_info):
    """Return a dict of base trope info

    Format will be the following
        tropeId -> {
            id:
            name:
            gender:
            image_url:
        }
    """
    info = extended_info(male_trope_info, male_image_info, female_trope_info, female_image_info)

    for k, v in info.iteritems():
        del v['description']
    return info

def extended_info(male_trope_info, male_image_info, female_trope_info, female_image_info):
    """Return a dict of extended trope info.

    Format will be the following
        tropeId -> {
            id:
            name:
            description:
            gender:
            image_url:
        }
    """

    male_image_map = {trope[0]: trope[1] for trope in male_image_info}
    female_image_map = {trope[0]: trope[1] for trope in female_image_info}

    male_trope_map = {trope[0]: trope[1] for trope in male_trope_info}
    female_trope_map = {trope[0]: trope[1] for trope in female_trope_info}

    results = dict()
    for k, v in male_trope_map.iteritems():
        results[k] = {
            'id': k,
            'name': to_name(k),
            'description': v,
            'gender': 'm',
            'image_url': image_url(k, male_image_map[k])
        }


    for k, v in female_trope_map.iteritems():
        results[k] = {
            'id': k,
            'name': to_name(k),
            'description': v,
            'gender': 'f',
            'image_url': image_url(k, female_image_map[k])
        }

    return results


if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Generate the info dict for tropes')
    parser.add_argument('--dest', help='source file', required=True)
    parser.add_argument('--filter', required=False)
    parser.add_argument('--extended', required=False, action='store_true')

    args = parser.parse_args()

    male_image_info = util.read_json('data/results/images/male/results.json')
    female_image_info = util.read_json('data/results/images/female/results.json')

    male_trope_info = util.read_json('data/results/male_only_tropes.json')
    female_trope_info = util.read_json('data/results/female_only_tropes.json')

    if args.filter:
        filter_list = util.read_json(args.filter)
        male_trope_info = [t for t in male_trope_info if t[0] in filter_list]
        female_trope_info = [t for t in female_trope_info if t[0] in filter_list]

    if args.extended:
        res = extended_info(male_trope_info, male_image_info, female_trope_info, female_image_info)
        util.write_json(args.dest, res)
    else:
        res = basic_info(male_trope_info, male_image_info, female_trope_info, female_image_info)
        util.write_json(args.dest, res)
