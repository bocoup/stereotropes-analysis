all: movie corpus
corpus: data/results/base_corpus.json data/results/female_corpus.json data/results/male_corpus.json

movie: movie_roles movie_categories movie_tropes trope_movies movie_metadata
movie_metadata: data/results/films.json
movie_roles: data/results/female_film_roles.json data/results/male_film_roles.json
movie_categories: data/results/female_film_categories.json data/results/male_film_categories.json
trope_movies: data/results/female_trope_films.json data/results/male_trope_films.json
movie_tropes: data/results/female_film_tropes.json data/results/male_film_tropes.json

analyse: analysis_dir log_likelyhood
analysis_dir:
	mkdir -p data/analysis

cluster: data/analysis/female_trope_clusters.json data/analysis/male_trope_clusters.json data/analysis/all_trope_clusters.json
log_likelyhood: data/analysis/male_ll.json data/analysis/female_ll.json data/analysis/male_trope_ll.json data/analysis/female_trope_ll.json

data/analysis/male_ll.json: data/results/base_corpus.json data/results/male_corpus.json
	python analyse_data.py --command log_likelyhood --source data/results/male_corpus.json data/results/base_corpus.json --dest $@
	touch $@
data/analysis/female_ll.json: data/results/base_corpus.json data/results/female_corpus.json
	python analyse_data.py --command log_likelyhood --source data/results/female_corpus.json data/results/base_corpus.json --dest $@
	# touch $@

data/analysis/female_trope_clusters.json: data/results/female_tropes_adjectives.json
	python analyse_data.py --command cluster --source data/results/female_tropes_adjectives.json --dest $@ --num_clusters 20
data/analysis/male_trope_clusters.json: data/results/male_tropes_adjectives.json
	python analyse_data.py --command cluster --source data/results/male_tropes_adjectives.json --dest $@ --num_clusters 20
data/analysis/all_trope_clusters.json: data/results/male_tropes_adjectives.json data/results/female_tropes_adjectives.json
	python analyse_data.py --command cluster --source data/results/male_tropes_adjectives.json data/results/female_tropes_adjectives.json --dest $@ --num_clusters 20
	touch $@

data/analysis/male_trope_ll.json: data/results/base_corpus.json data/results/male_tropes_adjectives.json
	python analyse_data.py --command trope_log_likelyhood --source data/results/male_tropes_adjectives.json data/results/base_corpus.json --dest $@
	touch $@
data/analysis/female_trope_ll.json: data/results/base_corpus.json data/results/female_tropes_adjectives.json
	python analyse_data.py --command trope_log_likelyhood --source data/results/female_tropes_adjectives.json data/results/base_corpus.json --dest $@
	touch $@

# Trope extraction
data/results/female_tropes.json: data/raw/FemaleTropesWithDescription.json
	mkdir -p data/results
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@
data/results/male_tropes.json: data/raw/MaleTropesWithDescription.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@
data/results/unisex_tropes.json: data/raw/UnisexTropesWithDescription.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch $@

# Category Filtering
data/results/female_only_tropes.json: data/results/female_tropes.json data/results/unisex_tropes.json
	python process_tropes.py --command filter_tropes --source data/results/female_tropes.json data/results/unisex_tropes.json --dest $@
	touch $@
data/results/male_only_tropes.json: data/results/male_tropes.json data/results/unisex_tropes.json
	python process_tropes.py --command filter_tropes --source data/results/male_tropes.json data/results/unisex_tropes.json --dest $@
	touch $@


# Film role extraction
data/results/female_film_roles.json: data/raw/FemaleTropeMovieRoles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/FemaleTropeMovieRoles.json data/raw/FilmSeries.json --dest $@
		touch $@
data/results/male_film_roles.json: data/raw/MaleTropeMovieRoles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_trope_tuples --source data/raw/MaleTropeMovieRoles.json data/raw/FilmSeries.json  --dest $@
		touch $@

# Film extraction
data/results/films.json: data/results/female_film_roles.json data/results/male_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_films --source data/results/female_film_roles.json data/results/male_film_roles.json --dest $@
		touch $@

# Film Categories
data/results/female_film_categories.json: data/results/female_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_categories --source $< --dest $@
		touch $@
data/results/male_film_categories.json: data/results/male_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_categories --source $< --dest $@
		touch $@

# Trope -> films
data/results/female_trope_films.json: data/results/female_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source $< --dest $@
		touch $@

data/results/male_trope_films.json: data/results/male_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source $< --dest $@
		touch $@

# Film -> Tropes
data/results/female_film_tropes.json: data/results/female_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@

data/results/male_film_tropes.json: data/results/male_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_film_tropes --source $< --dest $@
		touch $@

#Trope tagging
data/results/female_tropes_tagged.json: data/results/female_only_tropes.json
	mkdir -p data/results
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@
data/results/male_tropes_tagged.json: data/results/male_only_tropes.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@
data/results/unisex_tropes_tagged.json: data/results/unisex_tropes.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@


#Adjective extraction
data/results/female_tropes_adjectives.json: data/results/female_tropes_tagged.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@
data/results/male_tropes_adjectives.json: data/results/male_tropes_tagged.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@
data/results/unisex_tropes_adjectives.json: data/results/unisex_tropes_tagged.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@

#Make corpora for 3 main large groups. All adjectives, all female and all male.
data/results/base_corpus.json: data/results/female_tropes_adjectives.json data/results/male_tropes_adjectives.json
	python process_tropes.py --command make_base_corpus --source data/results/female_tropes_adjectives.json data/results/male_tropes_adjectives.json --dest $@
	touch $@

data/results/female_corpus.json: data/results/female_tropes_adjectives.json
	python process_tropes.py --command make_base_corpus --source data/results/female_tropes_adjectives.json --dest $@
	touch $@

data/results/male_corpus.json: data/results/male_tropes_adjectives.json
	python process_tropes.py --command make_base_corpus --source data/results/male_tropes_adjectives.json --dest $@
	touch $@