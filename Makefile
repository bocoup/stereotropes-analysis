all: movie corpus
corpus: data/results/base_corpus.json data/results/corpus-female.json data/results/corpus-male.json

movie: movie_roles movie_categories trope_movies movie_metadata
movie_metadata: data/results/films.json
movie_roles: data/results/film_roles-female.json data/results/film_roles-male.json
movie_categories: data/results/film_categories.json
trope_movies: data/results/trope_films-female.json data/results/trope_films-male.json

analyse: analysis_dir log_likelyhood
analysis_dir:
	mkdir -p data/analysis

cluster: data/analysis/trope_clusters-female.json data/analysis/male_trope_clusters.json data/analysis/all_trope_clusters.json
log_likelyhood: data/analysis/ll-male.json data/analysis/ll-female.json data/analysis/trope_ll-male.json data/analysis/trope_ll-female.json

data/analysis/ll-male.json: data/results/base_corpus.json data/results/corpus-male.json
	python analyse_data.py --command log_likelyhood --source data/results/corpus-male.json data/results/base_corpus.json --dest $@
	touch $@
data/analysis/ll-female.json: data/results/base_corpus.json data/results/corpus-female.json
	python analyse_data.py --command log_likelyhood --source data/results/corpus-female.json data/results/base_corpus.json --dest $@
	# touch $@

data/analysis/trope_clusters-female.json: data/results/tropes_adjectives-female.json
	python analyse_data.py --command cluster --source data/results/tropes_adjectives-female.json --dest $@ --num_clusters 40
data/analysis/male_trope_clusters.json: data/results/tropes_adjectives-male.json
	python analyse_data.py --command cluster --source data/results/tropes_adjectives-male.json --dest $@ --num_clusters 40
data/analysis/all_trope_clusters.json: data/results/tropes_adjectives-male.json data/results/tropes_adjectives-female.json
	python analyse_data.py --command cluster --source data/results/tropes_adjectives-male.json data/results/tropes_adjectives-female.json --dest $@ --num_clusters 40
	touch $@

data/analysis/trope_ll-male.json: data/results/base_corpus.json data/results/tropes_adjectives-male.json
	python analyse_data.py --command trope_log_likelyhood --source data/results/tropes_adjectives-male.json data/results/base_corpus.json --dest $@
	touch $@
data/analysis/trope_ll-female.json: data/results/base_corpus.json data/results/tropes_adjectives-female.json
	python analyse_data.py --command trope_log_likelyhood --source data/results/tropes_adjectives-female.json data/results/base_corpus.json --dest $@
	touch $@

# Trope extraction
data/results/tropes-female.json: data/raw/TropesWithDescription-Female.json
	mkdir -p data/results
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@
data/results/tropes-male.json: data/raw/TropesWithDescription-Male.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@
data/results/tropes-unisex.json: data/raw/TropesWithDescription-Unisex.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@

# Category Filtering
data/results/only_tropes-female.json: data/results/tropes-female.json data/results/tropes-unisex.json
	python process_tropes.py --command filter_tropes --source data/results/tropes-female.json data/results/tropes-unisex.json --dest $@
	touch $@
data/results/only_tropes-male.json: data/results/tropes-male.json data/results/tropes-unisex.json
	python process_tropes.py --command filter_tropes --source data/results/tropes-male.json data/results/tropes-unisex.json --dest $@
	touch $@

# Film role extraction
data/results/film_roles-female.json: data/raw/FilmTropeRoles-Female.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Female.json data/raw/FilmSeries.json --dest $@
		touch $@
data/results/film_roles-male.json: data/raw/FilmTropeRoles-Male.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/FilmTropeRoles-Male.json data/raw/FilmSeries.json  --dest $@
		touch $@

# Film -> (tropes by gender, film categories)
data/results/films.json: data/raw/Films.json data/results/film_roles-female.json data/results/film_roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_films --source data/raw/Films.json data/results/film_roles-female.json data/results/film_roles-male.json --dest $@
		touch $@

# Film Categories -> (tropes, films, counts)
data/results/film_categories.json: data/results/films/full_with_rt.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_categories --source $< --dest $@
		touch $@

# Trope -> films
data/results/trope_films-female.json: data/results/films/full_with_rt.json data/results/film_roles-female.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/film_roles-female.json --dest $@
		touch $@

data/results/trope_films-male.json: data/results/films/full_with_rt.json data/results/film_roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source data/results/films/full_with_rt.json data/results/film_roles-male.json --dest $@
		touch $@

# Film -> Tropes
data/results/film_tropes-female.json: data/results/film_roles-female.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@

data/results/film_tropes-male.json: data/results/film_roles-male.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@

#Trope tagging
data/results/tropes_tagged-female.json: data/results/only_tropes-female.json
	mkdir -p data/results
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@
data/results/tropes_tagged-male.json: data/results/only_tropes-male.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@
data/results/tropes_tagged-unisex.json: data/results/tropes-unisex.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@


#Adjective extraction
data/results/tropes_adjectives-female.json: data/results/tropes_tagged-female.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@
data/results/tropes_adjectives-male.json: data/results/tropes_tagged-male.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@
data/results/tropes_adjectives-unisex.json: data/results/tropes_tagged-unisex.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@

#Make corpora for 3 main large groups. All adjectives, all female and all male.
data/results/base_corpus.json: data/results/tropes_adjectives-female.json data/results/tropes_adjectives-male.json
	python process_tropes.py --command make_base_corpus --source data/results/tropes_adjectives-female.json data/results/tropes_adjectives-male.json --dest $@
	touch $@

data/results/corpus-female.json: data/results/tropes_adjectives-female.json
	python process_tropes.py --command make_base_corpus --source data/results/tropes_adjectives-female.json --dest $@
	touch $@

data/results/corpus-male.json: data/results/tropes_adjectives-male.json
	python process_tropes.py --command make_base_corpus --source data/results/tropes_adjectives-male.json --dest $@
	touch $@


#Download images for Tropes

images_female:
	mkdir -p data/results/images/female
	python process_tropes.py --command get_images --source data/results/only_tropes-female.json --dest data/results/images/female

images_male:
	mkdir -p data/results/images/male
	python process_tropes.py --command get_images --source data/results/only_tropes-male.json --dest data/results/images/male

#Download data for films


film: film_details

# - Scrabe omdb
data/results/films/full.json: data/results/films.json
	echo "Collecting OMDB Data"
	mkdir -p data/results/films
	python -m src.film.omdb --dest=data/results/films/full.json --src=data/results/films.json

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
data/results/films/films_with_similarity.json: data/results/films/full_with_posters.json
		echo "Adding film similarity"
		mkdir -p data/results
		python process_tropes.py --command find_similar_films --source data/results/films/full_with_posters.json --dest data/results/films/films_with_similarity.json
		touch $@

# - Download posters based on rotten tomato details
film_details: data/results/films/films_with_similarity.json data/results/film_roles-male.json data/results/film_roles-female.json
	echo "Building detail film files"
	mkdir -p data/production/films/details
	python -m src.film.detail --src=data/results/films/films_with_similarity.json \
		--dest=data/production/films/details \
		--roles data/results/film_roles-female.json \
		--roles data/results/film_roles-male.json \
		--extended=True


