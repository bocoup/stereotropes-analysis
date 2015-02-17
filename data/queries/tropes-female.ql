PREFIX dbt: <http://dbtropes.org/resource/Main/>
PREFIX rel: <http://skipforward.net/skipforward/resource/seeder/skipinions>
PREFIX ont: <http://dbtropes.org/ont/>
PREFIX schema: <http://www.w3.org/2000/01/rdf-schema#>


select $trope $comment
WHERE {
  $trope ont:processingCategory2 dbt:AlwaysFemale .
  OPTIONAL {
    $trope schema:comment $comment .
  }
}