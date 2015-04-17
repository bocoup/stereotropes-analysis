# Stereotropes-analysis

Scripts used to generate and process the data used for [Stereotropes](stereotropes.bocoup.com).

## About

Set of tools written in python to extract data from DB Tropes and perform text analysis on it.
This repo is also used to mash up film information from Rotten Tomatoes and IMDB with the TV Tropes data.


The data pipeline is controlled by a set of Makefiles.

 - tropes.mk
 - films.mk
 - production.mk

These in turn execute the python scripts needed to generate data for Stereotropes.

`tropes.mk` performs trope related tasks. Tropes are extracted from raw sparql files. Images for tropes are downloaded from TV Tropes. Tropes are filtered to remove unisex tropes. Words in trope descriptions are tagged and adjectives extracted.

`films.mk` performs film related tasks. Film details are extracted from IMDB and rotten tomatoes. Mappings between films and tropes are generated.

`production.mk` produces data needed in the client for its visualization and exploration capabilities. Film lists and trope lists are generated. Adjective lists are created.

## Running

```
make film_details -f production.mk
```
