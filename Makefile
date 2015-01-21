all: data/results/base_corpus.json data/results/female_corpus.json data/results/male_corpus.json data/results/unisex_tropes_adjectives.json

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