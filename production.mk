# Make file for production data for the gendertropes vis.
# These tasks output data in the format we are going to pipe
# down to the client.

#
# Shared Variables
#
output_dir = data/production

#
# Trope info map
#
dicts: $(output_dir)/trope_dict.json

$(output_dir)/trope_dict.json:
	python trope_dictionary.py --dest $@


#
# Trope lists (just the trope ids)
#
lists: $(output_dir)/trope_list_all.json $(output_dir)/trope_list_top_100_ll.json $(output_dir)/trope_list_top_100_count.json

$(output_dir)/trope_list_all.json:
	python tropes.py --dest $@

$(output_dir)/trope_list_top_100_ll.json:
	python tropes.py --by_ll --dest $@

$(output_dir)/trope_list_top_100_count.json:
	python tropes.py --by_film_occurence --dest $@


#
# Adjective page data
#

adjectives: $(output_dir)/adjectives_network.json

$(output_dir)/adjectives_network.json:
	python -m src.adjectives.adjectives --dest $@

#
# Gender splits page data
#

gender_split: $(output_dir)/gender_splits.json

$(output_dir)/gender_splits.json:
	python -m src.adjectives.gender_splits --dest $@