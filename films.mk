#
# Make file for film related tasks
#
# Other than top level tasks, tasks are split into three categorie
#
# 	Extract — extraction of data from the raw sparql query files and basic filtering
# 	Download - Downloading/scraping data from remote sources
# 	Analyse - Running analysis like NLP tasks, log likelyhood etc.
#
# Top level tasks try and summarize the main steps from each section.
# into tasks we may want to call directly without specifying the destination file(s).
#

#####################
# Shared variables
#####################

# RESULTS_DIR = data/results
# ANALYSIS_DIR = data/analysis

#####################
# Top Level tasks
#####################


movie_metadata: data/results/films/raw.json
movie_roles: data/results/films/roles-female.json data/results/films/roles-male.json

# We do not seem to use categories at the moment?
movie_categories: data/results/films/categories.json
trope_movies: data/results/films/trope_films-female.json data/results/films/trope_films-male.json

extract: movie_roles movie_metadata
download: data/results/films/full_with_posters.json
analyse: trope_movies movie_categories data/results/films/full_with_similarity.json

#####################
# Extract
#####################


# Film data extraction from raw sparql results

# Film role extraction
data/results/films/roles-female.json: data/raw/FilmTropeRoles-Female.json
	mkdir -p data/results
	python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Female.json data/raw/FilmSeries.json --dest $@
	touch $@
data/results/films/roles-male.json: data/raw/FilmTropeRoles-Male.json
	mkdir -p data/results
	python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Male.json data/raw/FilmSeries.json  --dest $@
	touch $@

# Produce a map of Film -> (tropes by gender, film categories)
data/results/films/raw.json: data/raw/Films.json data/results/films/roles-female.json data/results/films/roles-male.json
	mkdir -p data/results
	python process_tropes.py --command extract_films --source data/raw/Films.json data/results/films/roles-female.json data/results/films/roles-male.json --dest $@
	touch $@


#####################
# Download
#####################


# - Scrabe omdb
data/results/films/full.json: data/results/films/raw.json
	echo "Collecting OMDB Data"
	mkdir -p data/results/films
	python -m src.film.omdb --dest=data/results/films/full.json --src=data/results/films/raw.json
	touch $@

# - Scrape rotten tomatoes for metadata
data/results/films/full_with_rt.json: data/results/films/full.json
	echo "Collecting rotten tomato data"
	mkdir -p data/results/films/posters
	python -m src.film.posters --src=data/results/films/full.json --dest=data/results/films/full_with_rt.json \
		--scrape --failed=data/results/films/failed.json --poster_dest=data/production/films/posters/
	touch $@

# Download posters
data/results/films/full_with_posters.json: data/results/films/full_with_rt.json
	echo "Downloading Posters"
	mkdir -p data/results/films/posters
	python -m src.film.posters --src=data/results/films/full_with_rt.json --dest=data/results/films/full_with_posters.json \
		--failed=data/results/films/failed.json --poster_dest=data/production/films/posters/
	touch $@

#####################
# Analyse
#####################

# Produce a map of Film Categories -> (tropes, films, counts)
data/results/films/categories.json: data/results/films/full_with_rt.json
	mkdir -p data/results/films
	python process_tropes.py --command extract_film_categories --source $< --dest $@
	touch $@

# Produce maps of Tropes -> films
data/results/films/trope_films-female.json: data/results/films/full_with_rt.json data/results/films/roles-female.json
	mkdir -p data/results/films
	python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/films/roles-female.json --dest $@
	touch $@

data/results/films/trope_films-male.json: data/results/films/full_with_rt.json data/results/films/roles-male.json
	mkdir -p data/results/films
	python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/films/roles-male.json --dest $@
	touch $@

# Produce maps of Film -> Tropes
data/results/films/film_tropes-female.json: data/results/films/roles-female.json
	mkdir -p data/results/films
	python process_tropes.py --command extract_film_tropes --source $< --dest $@
	touch $@

data/results/films/film_tropes-male.json: data/results/films/roles-male.json
	mkdir -p data/results/films
	python process_tropes.py --command extract_film_tropes --source $< --dest $@
	touch $@

# Compute similarity of films based on co-occuring tropes
data/results/films/full_with_similarity.json: data/results/films/full_with_posters.json
	echo "Adding film similarity"
	mkdir -p data/results/films
	python process_tropes.py --command find_similar_films --source data/results/films/full_with_posters.json --dest data/results/films/full_with_similarity.json
	touch $@

