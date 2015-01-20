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

    parser = argparse.ArgumentParser(description='Apply NLTK POS tagging to a text')

    parser.add_argument('--source', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--dest', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()

    target_text =  string.join(args.source.readlines())
    result = tag(target_text)

    args.dest.write(json.dumps(result, indent=4))