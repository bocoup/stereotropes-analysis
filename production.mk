# Make file for production data for the gendertropes vis.


all: dicts

dicts: data/production/trope_dict.json

data/production/trope_dict.json:
	python trope_dictionary.py --dest $@

