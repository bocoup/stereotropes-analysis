#
# Top level makefile for gendertropes project.
#
# This file contains top level data generation tasks for gendertropes.
# The actual data generation steps are actually specified in the following
# makefiles which this makefile merely shells to.
# 	tropes.mk —  pre-production tasks for trope related data
# 	films.mk - pre-production tasks for film related data
#		production.mk - tasks that produce the production files for the final visualization
#

#####################
# Top level tasks
#####################

tropes: extract_tropes analyse_tropes tropes_prod
tropes_with_download: extract_tropes download_trope_images analyse_tropes tropes_prod



#####################
# Trope Preprocessing Tasks
#####################

extract_tropes:
	make -f tropes.mk extract

download_trope_images:
	make -f tropes.mk download

analyse_tropes:
	make -f tropes.mk analyse

#####################
# Trope Production Tasks
#####################

tropes_prod:
	make -f production.mk dicts
	make -f production.mk lists
	make -f production.mk film_list
	make -f production.mk adjectives
	make -f production.mk gender_split



#####################
# Film Preprocessing Tasks
#####################

movie: movie_roles movie_categories trope_movies movie_metadata
movie_metadata: data/results/films/raw.json
movie_roles: data/results/films/roles-female.json data/results/films/roles-male.json
movie_categories: data/results/films/categories.json
trope_movies: data/results/films/trope_films-female.json data/results/films/trope_films-male.json

#####################
# Film Production Tasks
#####################


# Film role extraction
data/results/films/roles-female.json: data/raw/FilmTropeRoles-Female.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Female.json data/raw/FilmSeries.json --dest $@
		touch $@
data/results/films/roles-male.json: data/raw/FilmTropeRoles-Male.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Male.json data/raw/FilmSeries.json  --dest $@
		touch $@

# Film -> (tropes by gender, film categories)
data/results/films/raw.json: data/raw/Films.json data/results/films/roles-female.json data/results/films/roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_films --source data/raw/Films.json data/results/films/roles-female.json data/results/films/roles-male.json --dest $@
		touch $@

# Film Categories -> (tropes, films, counts)
data/results/films/categories.json: data/results/films/full_with_rt.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_categories --source $< --dest $@
		touch $@

# Trope -> films
data/results/films/trope_films-female.json: data/results/films/full_with_rt.json data/results/films/roles-female.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/films/roles-female.json --dest $@
		touch $@

data/results/films/trope_films-male.json: data/results/films/full_with_rt.json data/results/films/roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/films/roles-male.json --dest $@
		touch $@

# Film -> Tropes
data/results/films/film_tropes-female.json: data/results/films/roles-female.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@

data/results/films/film_tropes-male.json: data/results/films/roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@


#Download data for films


film: film_details

# - Scrabe omdb
data/results/films/full.json: data/results/films/raw.json
	echo "Collecting OMDB Data"
	mkdir -p data/results/films
	python -m src.film.omdb --dest=data/results/films/full.json --src=data/results/films/raw.json

# - Scrape rotten tomatoes for metadata
data/results/films/full_with_rt.json: data/results/films/full.json
	echo "Collecting rotten tomato data"
	mkdir -p data/results/films/posters
	python -m src.film.posters --src=data/results/films/full.json --dest=data/results/films/full_with_rt.json \
		--scrape --failed=data/results/films/failed.json --poster_dest=data/production/films/posters/

# Download posters
data/results/films/full_with_posters.json: data/results/films/full_with_rt.json
	echo "Downloading Posters"
	mkdir -p data/results/films/posters
	python -m src.film.posters --src=data/results/films/full_with_rt.json --dest=data/results/films/full_with_posters.json \
		--failed=data/results/films/failed.json --poster_dest=data/production/films/posters/

# - Compute similarity
data/results/films/full_with_similarity.json: data/results/films/full_with_posters.json
		echo "Adding film similarity"
		mkdir -p data/results
		python process_tropes.py --command find_similar_films --source data/results/films/full_with_posters.json --dest data/results/films/full_with_similarity.json
		touch $@

# - Download posters based on rotten tomato details
film_details: data/results/films/full_with_similarity.json data/results/films/roles-male.json data/results/films/roles-female.json
	echo "Building detail film files"
	mkdir -p data/production/films/details
	python -m src.film.detail --src=data/results/films/full_with_similarity.json \
		--dest=data/production/films/details \
		--roles data/results/films/roles-female.json \
		--roles data/results/films/roles-male.json \
		--extended=True


