PREFIX dbt: <http://dbtropes.org/resource/Main/>
PREFIX rel: <http://skipforward.net/skipforward/resource/seeder/skipinions>
PREFIX rdff: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://www.w3.org/2000/01/rdf-schema#>

select $trope $comment
WHERE {
  dbt:AlwaysMale rdff:seeAlso ?trope .
  OPTIONAL {
    $trope schema:comment $comment
  }

}