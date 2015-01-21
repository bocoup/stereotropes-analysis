all: movie corpus
corpus: data/results/base_corpus.json data/results/female_corpus.json data/results/male_corpus.json

movie: movie_roles movie_categories movie_tropes
movie_roles: data/results/female_film_roles.json data/results/male_film_roles.json
movie_categories: data/results/female_film_categories.json data/results/male_film_categories.json
movie_tropes: data/results/female_film_tropes.json data/results/male_film_tropes.json

# Trope extraction
data/results/female_tropes.json: data/raw/FemaleTropesWithDescription.json
		mkdir -p data/results
		python process_tropes.py --command extract_tropes --source $< --dest $@
		touch $@
data/results/male_tropes.json: data/raw/MaleTropesWithDescription.json
		python process_tropes.py --command extract_tropes --source $< --dest $@
		touch $@

# Film extraction
data/results/female_film_roles.json: data/raw/FemaleTropeMovieRoles.json
		mkdir -p data/results
		python process_tropes.py --command extract_films --source $< --dest $@
		touch $@
data/results/male_film_roles.json: data/raw/MaleTropeMovieRoles.json
		mkdir -p data/results
		python process_tropes.py --command extract_films --source $< --dest $@
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

# Film Tropes
data/results/female_film_tropes.json: data/results/female_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source $< --dest $@
		touch $@
data/results/male_film_tropes.json: data/results/male_film_roles.json
		mkdir -p data/results
		python process_tropes.py --command extract_trope_films --source $< --dest $@
		touch $@

#Trope tagging
data/results/female_tropes_tagged.json: data/results/female_tropes.json
	mkdir -p data/results
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@
data/results/male_tropes_tagged.json: data/results/male_tropes.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch $@

#Adjective extraction
data/results/female_tropes_adjectives.json: data/results/female_tropes_tagged.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch $@
data/results/male_tropes_adjectives.json: data/results/male_tropes_tagged.json
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