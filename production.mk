# Make file for production data for the gendertropes vis.
# These tasks output data in the format we are going to pipe
# down to the client.

#
# Shared Variables
#
output_dir = data/production

create_out:
	mkdir -p data/production

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

film_list: create_out $(output_dir)/film_list.json $(output_dir)/genres/all_top_100.json $(output_dir)/genres/genres.json $(output_dir)/genres/decades.json
$(output_dir)/film_list.json: data/results/films/full_with_similarity.json
	python -m src.film.list --src $< --dest $@

$(output_dir)/genres/all_top_100.json: data/results/films/full_with_similarity.json
	mkdir -p $(output_dir)/genres
	python -m src.film.list --src $< --dest $@ --top 100

$(output_dir)/genres/genres.json: data/results/films/full_with_similarity.json
	mkdir -p $(output_dir)/genres
	python -m src.film.list --src $< --dest $@ --genres true
	touch -c $(output_dir)/genres/genres.json

$(output_dir)/genres/decades.json: data/results/films/full_with_similarity.json
	mkdir -p $(output_dir)/genres
	python -m src.film.list --src $< --dest $@ --decades true
	touch -c $(output_dir)/genres/decades.json

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
	mkdir -p $(output_dir)/films/details
	python -m src.film.detail --src=data/results/films/full_with_similarity.json \
		--dest=data/production/films/details \
		--roles data/results/films/roles-female.json \
		--roles data/results/films/roles-male.json \
		--extended=True


#
# Trope details data
#
trope_details:
	echo "Building trope detail files"
	mkdir -p $(output_dir)/tropes/details
	python -m src.trope.detail --dest=$(output_dir)/tropes/details

#
# Clean tasks
#
clean:
	rm -rf data/production/*.json
	rm -rf data/production/genres/*.json
	rm -rf data/production/films/details/*.json
	rm -rf data/production/tropes/details/*.json
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
	rsync -a data/production/tropes/details/ $(target)/tropes/detail/
	rsync -a data/production/genres/ $(target)/films/genres/


