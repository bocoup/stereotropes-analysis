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
trope_dict: $(output_dir)/trope_dict.json

$(output_dir)/trope_dict.json:
	mkdir -p data/production
	python -m src.trope.trope_dictionary --dest $@


#
# Trope lists (just the trope ids)
#
trope_lists: $(output_dir)/trope_list_all.json $(output_dir)/trope_list_top_100_ll.json $(output_dir)/trope_list_top_100_count.json $(output_dir)/film_list.json

$(output_dir)/trope_list_all.json:
	python -m src.trope.trope_lists --dest $@

$(output_dir)/trope_list_top_100_ll.json:
	python -m src.trope.trope_lists --by_ll --dest $@

$(output_dir)/trope_list_top_100_count.json:
	python -m src.trope.trope_lists --by_film_occurence --dest $@

#
# Film lists
#

film_list: $(output_dir)/film_list.json
$(output_dir)/film_list.json: data/results/films/full_with_similarity.json
	python -m src.film.list --src $< --dest $@

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


#
# Film details data
#

film_details:
	echo "Building detail film files"
	mkdir -p data/production/films/details
	python -m src.film.detail --src=data/results/films/full_with_similarity.json \
		--dest=data/production/films/details \
		--roles data/results/films/roles-female.json \
		--roles data/results/films/roles-male.json \
		--extended=True


#
# Clean tasks
#
clean:
	rm -rf data/production/
	mkdir -p data/production

#
# Copy tasks
#

# This will sync the production files to their corresponding path in
# a target data directory. The target directory is expected to have
# the following structure of subdirs. It will use rsync to avoid
# unnecessary copies. The target folder should be passed in as
# a var to the makefile e.g. target=foo
#
# 	adjectives
# 	films
# 		details
# 		posters
# 	gender
# 	tropes
# 		detail
# 		images
copy:
	echo $(target)
	rsync -a data/production/trope_* $(target)/tropes
	rsync -a data/production/adjectives_network.json $(target)/adjectives
	rsync -a data/production/gender_splits.json $(target)/gender
	rsync -a data/production/films/details/ $(target)/films/detail/


