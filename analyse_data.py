import json
import os
import nltk
import pprint

def write_json(path, data):
    output = open(path, 'w')
    output.write(json.dumps(data, indent=4))
    output.close

def read_json(path):
    file = open(os.path.abspath(path), 'r')
    data = json.load(file)
    file.close
    return data

def pp(data):
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(data)

# from http://nbviewer.ipython.org/github/Prooffreader/Misc_ipynb/blob/master/billboard_charts/billboard_top_words.ipynb
def loglike(n1, t1, n2, t2):
    """Calculates Dunning log likelihood of an observation of
    frequency n1 in a corpus of size t1, compared to a frequency n2
    in a corpus of size t2. If result is positive, it is more
    likely to occur in corpus 1, otherwise in corpus 2."""
    from numpy import log
    e1 = t1*1.0*(n1+n2)/(t1+t2) # expected values
    e2 = t2*1.0*(n1+n2)/(t1+t2)
    LL = 2 * ((n1 * log(n1/e1)) + n2 * (log(n2/e2)))
    if n2*1.0/t2 > n1*1.0/t1:
        LL = -LL
    return LL

def compute_LL(source_corpus, background_corpus):

	sc = [s.lower() for s in source_corpus]
	bc = [s.lower() for s in background_corpus]

	background_freq = nltk.FreqDist(bc)
	source_freq = nltk.FreqDist(sc)

	source_len = len(sc)
	bg_len = len(bc)

	results = []

	for word, count in source_freq.items():
		ll = loglike(count, source_len, background_freq[word], bg_len)
		results.append((word, count, ll))

	sorted_ll = sorted(results, key=lambda tup: tup[2], reverse=True)
	# pp(sorted_ll[0:20])

	return sorted_ll


def normalize_LL(source):
	'''Once LL's are computed, we normalize them to a scale.
		 Because of how we are constructing our background_corpus
		 as the concatenation of the two corpora we are trying to
		 compare a value will not be positive or negative
		 in both the lists. So we will normalize each sign individually,
		 i.e. values below 0 will be normalized to the range -1 to 0
		 and values above 0 will be normalized to the range 1 to 0.

		 I'm not sure if this holds in cases where the background corpus
		 is not a concatenation of the two source curpora. This has
		 only been checked for the male and female LL results'''

	vals = [tup[2] for tup in source]

	min_val = min(vals)
	max_val = max(vals)

	results = []
	for word, count, ll in source:
		if ll <= 0:
			norm = -(ll / min_val)
		else:
			norm = ll / max_val
		results.append((word, count, ll, norm))

	return results


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

    if args.command == 'log_likelyhood':
    	# expected input is a json array of tokens (words)
        source_corpus = read_json(args.source[0])
        background_corpus = read_json(args.source[1])

        result = normalize_LL(compute_LL(source_corpus, background_corpus))
        write_json(args.dest, result)
    if args.command == 'trope_log_likelyhood':
        # expected input is an array containing tuples
        tropes_corpus = read_json(args.source[0])
        background_corpus = read_json(args.source[1])

        for trope in tropes_corpus:
            trope_name = trope[0]
            trope_adjectives = trope[1]

            if len(trope_adjectives) > 1:

                ll = compute_LL(trope_adjectives, background_corpus)
                normalized_ll = normalize_LL(ll)

                trope[1] = normalized_ll

        write_json(args.dest, tropes_corpus)


    else:
        print('Unknown Command')


