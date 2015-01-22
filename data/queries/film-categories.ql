PREFIX ont: <http://dbtropes.org/ont/>
PREFIX main: <http://dbtropes.org/resource/Main/>

SELECT * WHERE
{
{
    SELECT $genre WHERE
    {
         $genre ont:processingCategory2 main:FilmsOfThe2000s
    }
}
UNION
{
    SELECT $genre
    {
         $genre ont:processingCategory2 main:Film
    }
}
}