PREFIX dbt: <http://dbtropes.org/resource/Main/>
PREFIX ont: <http://dbtropes.org/ont/>

SELECT $series WHERE {
  $series ont:processingCategory1 dbt:FilmSeries
}
