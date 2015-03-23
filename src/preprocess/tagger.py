from nltk import word_tokenize
from nltk import pos_tag
from collections import defaultdict


def tag(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    grouped_tags = defaultdict(list)
    for token, tag in tagged:
        grouped_tags[tag].append(token)

    return {
        'tagged': tagged,
        'by_tag': dict(grouped_tags)
    }

if __name__ == "__main__":
    import argparse
    import sys
    import json
    import string
    import os

    parser = argparse.ArgumentParser(description='Apply NLTK POS tagging to a text')

    # parser.add_argument('--source', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    # parser.add_argument('--dest', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    parser.add_argument('--source', nargs='?', default=sys.stdin)
    parser.add_argument('--dest', nargs='?', default=sys.stdout)

    args = parser.parse_args()

    source = args.source
    dest = args.dest

    if source != sys.stdin and os.path.isdir(source) and os.path.isdir(dest):
        for fp in os.listdir(source):
            source_file = open(os.path.join(source, fp), 'r')
            target_text = string.join(source_file.readlines())

            result = tag(target_text)

            dest_file = open(os.path.join(dest, fp), 'w')
            dest_file.write(json.dumps(result, indent=4))

            source_file.close()
            dest_file.close()

        print "process directory"
    else:
        if isinstance(source, str):
            source = open(source, 'r')
        if isinstance(dest, str):
            dest = open(dest, 'w')

        target_text =  string.join(source.readlines())
        result = tag(target_text)
        dest.write(json.dumps(result, indent=4))
