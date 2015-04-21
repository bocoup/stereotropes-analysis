# Stereotropes Analysis

This repository is a companion for the [Stereotropes](stereotropes.bocoup.com)
project.

Stereotropes is an interactive experiment, exploring a set of tropes authored
by the community on http://tvtropes.org that are categorized as being always
female or always male.

The scripts in this repository are used to generate the data
used to power the Stereotropes application. Some of this data can be found here:

http://github.com/bocoup/stereotropes-data-public

The code utilizing this data lives at:

http://github.com/bocoup/stereotropes-client

## About

This repository contains a set of tools written in python to extract data from
several sources including [DB Tropes](http://dbtropes.org), [OMDB](http://omdbapi.com)
and [Rotten Tomatoes](http://rottentomatoes.com).

These scripts:

* collects adjectives from trope discriptions
* explore the gender balance of language used to describe tropes through the log likelihood method
* collect metadata about tropes
* collect metadata about films
* explore connections between tropes through adjective use
* explore connections between films through use of tropes

The data pipeline is controlled by a set of Makefiles.

 - `tropes.mk`
 - `films.mk`
 - `production.mk`

These in turn execute the python scripts needed to generate data for Stereotropes.

`tropes.mk` performs trope related tasks. Tropes are extracted from raw sparql
files. Images for tropes are downloaded from TV Tropes. Tropes are filtered to
remove unisex tropes. Words in trope descriptions are tagged and adjectives
extracted.

`films.mk` performs film related tasks. Film details are extracted from IMDB
and rotten tomatoes. Mappings between films and tropes are generated.

`production.mk` produces data needed in the client for its visualization and
exploration capabilities. Film lists and trope lists are generated.
Adjective lists are created.

## Running

```
make film_details -f production.mk
```

## Resources

We learned a lot about Log Liklihood from this fantastic [iPython Notebook](http://nbviewer.ipython.org/github/Prooffreader/Misc_ipynb/blob/master/billboard_charts/billboard_top_words.ipynb) put together
for the the analysis and visualization article "[Most Decade-specific words in Billboard popular song titles, 1980 - 2014](http://www.prooffreader.com/2014/12/most-decade-specific-words-in-billboard.html)".
