#
# Make file for trope related tasks
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

RESULTS_DIR = data/results
ANALYSIS_DIR = data/analysis

#####################
# Top Level tasks
#####################

extract: $(RESULTS_DIR)/only_tropes-female.json $(RESULTS_DIR)/only_tropes-male.json
download: images_female images_male
analyse: corpus log_likelyhood

#####################
# Extract
#####################


# Trope extraction from raw sparql files
$(RESULTS_DIR)/tropes-female.json: data/raw/TropesWithDescription-Female.json
	mkdir -p $(RESULTS_DIR)
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch -c $@
$(RESULTS_DIR)/tropes-male.json: data/raw/TropesWithDescription-Male.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch -c $@
$(RESULTS_DIR)/tropes-unisex.json: data/raw/TropesWithDescription-Unisex.json
	python process_tropes.py --command extract_tropes --source $< --dest $@
	touch -c $@

# Category Filtering, removes unisex tropes from the female and male lists of tropes.
$(RESULTS_DIR)/only_tropes-female.json: $(RESULTS_DIR)/tropes-female.json $(RESULTS_DIR)/tropes-unisex.json
	python process_tropes.py --command filter_tropes --source $(RESULTS_DIR)/tropes-female.json $(RESULTS_DIR)/tropes-unisex.json --dest $@
	touch -c $@
$(RESULTS_DIR)/only_tropes-male.json: $(RESULTS_DIR)/tropes-male.json $(RESULTS_DIR)/tropes-unisex.json
	python process_tropes.py --command filter_tropes --source $(RESULTS_DIR)/tropes-male.json $(RESULTS_DIR)/tropes-unisex.json --dest $@
	touch -c $@



#####################
# Download
#
# Note: these tasks do not specify dependencies, they will always run when called.
#####################

images_female:
	mkdir -p $(RESULTS_DIR)/images/female
	python process_tropes.py --command get_images --source $(RESULTS_DIR)/only_tropes-female.json --dest $(RESULTS_DIR)/images/female

images_male:
	mkdir -p $(RESULTS_DIR)/images/male
	python process_tropes.py --command get_images --source $(RESULTS_DIR)/only_tropes-male.json --dest $(RESULTS_DIR)/images/male


#####################
# Analyse
#####################

corpus: $(RESULTS_DIR)/base_corpus.json $(RESULTS_DIR)/corpus-female.json $(RESULTS_DIR)/corpus-male.json
log_likelyhood: $(ANALYSIS_DIR)/ll-male.json $(ANALYSIS_DIR)/ll-female.json $(ANALYSIS_DIR)/trope_ll-male.json $(ANALYSIS_DIR)/trope_ll-female.json
cluster: $(ANALYSIS_DIR)/trope_clusters-female.json $(ANALYSIS_DIR)/male_trope_clusters.json $(ANALYSIS_DIR)/all_trope_clusters.json

#
# Trope NLP tagging
#
$(RESULTS_DIR)/tropes_tagged-female.json: $(RESULTS_DIR)/only_tropes-female.json
	mkdir -p $(RESULTS_DIR)
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch -c $@
$(RESULTS_DIR)/tropes_tagged-male.json: $(RESULTS_DIR)/only_tropes-male.json
	python process_tropes.py --command tag_tropes --source $< --dest $@
	touch -c $@

#
# Adjective extraction
#
$(RESULTS_DIR)/tropes_adjectives-female.json: $(RESULTS_DIR)/tropes_tagged-female.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch -c $@
$(RESULTS_DIR)/tropes_adjectives-male.json: $(RESULTS_DIR)/tropes_tagged-male.json
	python process_tropes.py --command extract_adjectives --source $< --dest $@
	touch -c $@

#
# Make corpora for 3 main large groups. All adjectives, all female and all male.
#
$(RESULTS_DIR)/base_corpus.json: $(RESULTS_DIR)/tropes_adjectives-female.json $(RESULTS_DIR)/tropes_adjectives-male.json
	python process_tropes.py --command make_base_corpus --source $(RESULTS_DIR)/tropes_adjectives-female.json $(RESULTS_DIR)/tropes_adjectives-male.json --dest $@
	touch -c $@

$(RESULTS_DIR)/corpus-female.json: $(RESULTS_DIR)/tropes_adjectives-female.json
	python process_tropes.py --command make_base_corpus --source $(RESULTS_DIR)/tropes_adjectives-female.json --dest $@
	touch -c $@

$(RESULTS_DIR)/corpus-male.json: $(RESULTS_DIR)/tropes_adjectives-male.json
	python process_tropes.py --command make_base_corpus --source $(RESULTS_DIR)/tropes_adjectives-male.json --dest $@
	touch -c $@


#
# Calculate adjective log-likely hood for the two large corpora (all female adjs and all male adjs).
#
$(ANALYSIS_DIR)/ll-male.json: $(RESULTS_DIR)/base_corpus.json $(RESULTS_DIR)/corpus-male.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command log_likelyhood --source $(RESULTS_DIR)/corpus-male.json $(RESULTS_DIR)/base_corpus.json --dest $@
	touch -c $@
$(ANALYSIS_DIR)/ll-female.json: $(RESULTS_DIR)/base_corpus.json $(RESULTS_DIR)/corpus-female.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command log_likelyhood --source $(RESULTS_DIR)/corpus-female.json $(RESULTS_DIR)/base_corpus.json --dest $@
	touch -c $@

#
# Calculate adjective log-likely hood for each trope as compared to the base corpus of all adjectives.
#
$(ANALYSIS_DIR)/trope_ll-male.json: $(RESULTS_DIR)/base_corpus.json $(RESULTS_DIR)/tropes_adjectives-male.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command trope_log_likelyhood --source $(RESULTS_DIR)/tropes_adjectives-male.json $(RESULTS_DIR)/base_corpus.json --dest $@
	touch -c $@
$(ANALYSIS_DIR)/trope_ll-female.json: $(RESULTS_DIR)/base_corpus.json $(RESULTS_DIR)/tropes_adjectives-female.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command trope_log_likelyhood --source $(RESULTS_DIR)/tropes_adjectives-female.json $(RESULTS_DIR)/base_corpus.json --dest $@
	touch -c $@

#
# Cluster the tropes by adjective use
# (note: we do not currently use this analysis, this it will be not be run by the top level tasks)
#
$(ANALYSIS_DIR)/trope_clusters-female.json: $(RESULTS_DIR)/tropes_adjectives-female.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command cluster --source $(RESULTS_DIR)/tropes_adjectives-female.json --dest $@ --num_clusters 40
	touch -c $@
$(ANALYSIS_DIR)/male_trope_clusters.json: $(RESULTS_DIR)/tropes_adjectives-male.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command cluster --source $(RESULTS_DIR)/tropes_adjectives-male.json --dest $@ --num_clusters 40
	touch -c $@
$(ANALYSIS_DIR)/all_trope_clusters.json: $(RESULTS_DIR)/tropes_adjectives-male.json $(RESULTS_DIR)/tropes_adjectives-female.json
	mkdir -p $(ANALYSIS_DIR)
	python analyse_data.py --command cluster --source $(RESULTS_DIR)/tropes_adjectives-male.json $(RESULTS_DIR)/tropes_adjectives-female.json --dest $@ --num_clusters 40
	touch -c $@