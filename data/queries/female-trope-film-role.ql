PREFIX dbt: <http://dbtropes.org/resource/Main/>
PREFIX film:<http://dbtropes.org/resource/Main/Film/>
PREFIX rel: <http://skipforward.net/skipforward/resource/seeder/skipinions/>
PREFIX ont: <http://dbtropes.org/ont/>
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <http://www.w3.org/2000/01/rdf-schema#>


select $trope $film $label $film_category_label $role
WHERE {

  # select only tropes that are identified as Always Female
  $trope ont:processingCategory1 dbt:AlwaysFemale.
  OPTIONAL {

    # Get the ids of films that have this trope listed
    $film_id r:type $trope .

    # Get the role description from the film
    $film_id schema:comment $role .

    # Get the film page
    $film rel:hasFeature $film_id .

    # Get the film name (saved under label)
    $film schema:label $label .

    # Make sure that the type of "film" is actually a film by having been associated
    # with some form of a film category. We are excluding
    # Anime, Comic books, TV etc.
    $film ont:processingCategory1 $film_category .
    {{ $film_category ont:processingCategory2 dbt:Film } UNION { $film_category ont:processingCategory2 dbt:FilmsOfThe2000s }} .
    $film_category schema:label $film_category_label
  }
}
ORDER BY $trope