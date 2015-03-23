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

film: extract_films analyse_films film_prod
film_with_download: extract_films download_film_data analyse_films film_prod



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

extract_films:
	make -f films.mk extract

analyse_films:
	make -f films.mk analyse

download_film_data:
	make -f films.mk download


#####################
# Film Production Tasks
#####################

film_prod:
	make -f production.mk film_details













