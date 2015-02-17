PREFIX resource: <http://dbtropes.org/resource/>
PREFIX dbt: <http://dbtropes.org/resource/Main/>
PREFIX film:<http://dbtropes.org/resource/Main/Film/>
PREFIX rel: <http://skipforward.net/skipforward/resource/seeder/skipinions/>
PREFIX ont: <http://dbtropes.org/ont/>
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <http://www.w3.org/2000/01/rdf-schema#>

select DISTINCT $trope $film $label $role
WHERE {

  # select only tropes that are identified as Always Male
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
    $film ont:processingCategory1 $film_category
  }

    FILTER (
        $film_category IN (
         dbt:FilmsOfThe2000sFranchises,
         dbt:FilmsOf2000-2004,
         dbt:FilmsOf2005-2009,
         dbt:FilmsOfThe1970s,
         dbt:AnimatedFilms,
         dbt:FilmsOfThe1980s,
         dbt:FilmsOfThe1960s,
         dbt:FilmsOfThe2010s,
         dbt:FilmsOfThe1990s,
         dbt:FilmsOfThe2000s,
         dbt:FilmsOfThe1950s,
         dbt:FilmsOfThe1930s,
         dbt:FilmsOfThe1940s,
         dbt:EarlyFilms,
         dbt:FilmsOfThe1920s,
         dbt:FilmTropes,
         dbt:HomeVideoTropes,
         dbt:Nollywood,
         dbt:FantasyFilms,
         dbt:ScienceFictionFilms,
         dbt:HorrorFilms,
         dbt:FrenchFilms,
         dbt:IndexOfFilmWesterns,
         dbt:MysteryAndDetectiveFilms,
         dbt:TelevisionMovieIndex,
         dbt:HongKongFilms,
         dbt:MilitaryAndWarfareFilms,
         dbt:JapaneseFilms,
         dbt:RogerEbertMostHatedFilmList,
         dbt:KoreanMovies,
         dbt:BollywoodMovies,
         dbt:RiffTraxMovies,
         dbt:CzechFilms,
         dbt:BritishFilms,
         dbt:RussianFilms,
         dbt:ChineseFilms,
         dbt:GermanFilms,
         dbt:ItalianFilms,
         dbt:AFIS100Years100Movies,
         dbt:AFIS100Years100Movies10THAnniversaryEdition
        )
    &&
    $film  NOT IN (<http://dbtropes.org/resource/Anime/Pokemon>,
        <http://dbtropes.org/resource/Franchise/Godzilla>,
        <http://dbtropes.org/resource/Franchise/Batman>,
        <http://dbtropes.org/resource/Film/TheFastAndTheFurious>,
        <http://dbtropes.org/resource/Franchise/StarTrek>,
        <http://dbtropes.org/resource/WesternAnimation/LooneyTunes>,
        <http://dbtropes.org/resource/Film/TheThreeStooges>,
        <http://dbtropes.org/resource/WesternAnimation/TomAndJerry>,
        <http://dbtropes.org/resource/Film/HarryPotter>,
        <http://dbtropes.org/resource/Film/JamesBond>,
        <http://dbtropes.org/resource/Film/BackToTheFuture>,
        <http://dbtropes.org/resource/Film/FreeWilly>,
        <http://dbtropes.org/resource/Film/PoliceAcademy>,
        <http://dbtropes.org/resource/ComicStrip/Popeye>,
        <http://dbtropes.org/resource/Film/TheDarkKnightSaga>,
        <http://dbtropes.org/resource/Franchise/MarvelCinematicUniverse>,
        <http://dbtropes.org/resource/Franchise/Alien>,
        <http://dbtropes.org/resource/Film/TheExorcist>,
        <http://dbtropes.org/resource/Franchise/ANightmareOnElmStreet>,
        <http://dbtropes.org/resource/Film/Psycho>,
        <http://dbtropes.org/resource/Franchise/DieHard>,
        <http://dbtropes.org/resource/Main/Starwars>,
        <http://dbtropes.org/resource/Main/ThePhantomOfTheOpera>,
        <http://dbtropes.org/resource/Main/MickeyMouse>,
        <http://dbtropes.org/resource/Main/Zatoichi>,
        <http://dbtropes.org/resource/Main/Dracula>,
        <http://dbtropes.org/resource/Franchise/FridayThe13th>,
        <http://dbtropes.org/resource/Franchise/IndianaJones>,
        <http://dbtropes.org/resource/Franchise/Rambo>,
        <http://dbtropes.org/resource/Film/DeathWish>,
        <http://dbtropes.org/resource/Film/Poltergeist>,
        <http://dbtropes.org/resource/Film/ViolentShit>,
        <http://dbtropes.org/resource/Film/NightOfTheDemons>,
        <http://dbtropes.org/resource/Film/SleepawayCamp>,
        <http://dbtropes.org/resource/Film/ErnestPWorrell>,
        <http://dbtropes.org/resource/Film/SilentNightDeadlyNight>,
        <http://dbtropes.org/resource/Film/ReturnOfTheLivingDead>,
        <http://dbtropes.org/resource/Film/TheNakedGun>,
        <http://dbtropes.org/resource/Literature/DonCamillo>,
        <http://dbtropes.org/resource/Film/TheFly>,
        <http://dbtropes.org/resource/Film/TheHowling>,
        <http://dbtropes.org/resource/Film/TheOmen>,
        <http://dbtropes.org/resource/Film/TheAmityvilleHorror>,
        <http://dbtropes.org/resource/Film/DirtyHarry>,
        <http://dbtropes.org/resource/Film/IronEagle>,
        <http://dbtropes.org/resource/Franchise/TheTexasChainsawMassacre>,
        <http://dbtropes.org/resource/Franchise/StarWars>,
        <http://dbtropes.org/resource/Franchise/Hellraiser>,
        <http://dbtropes.org/resource/Franchise/Halloween>,
        <http://dbtropes.org/resource/Franchise/Gamera>,
        <http://dbtropes.org/resource/Franchise/ThePinkPanther>,
        <http://dbtropes.org/resource/Film/PromNight1980>,
        <http://dbtropes.org/resource/Franchise/Rocky>,
        <http://dbtropes.org/resource/Main/HammerHorror>,
        <http://dbtropes.org/resource/Main/CharlieChan>,
        <http://dbtropes.org/resource/Franchise/Zorro>,
        <http://dbtropes.org/resource/Film/AmericanPie>,
        <http://dbtropes.org/resource/Main/TheLittleRascals>,
        <http://dbtropes.org/resource/WesternAnimation/IceAge>,
        <http://dbtropes.org/resource/WesternAnimation/DonaldDuck>,
        <http://dbtropes.org/resource/WesternAnimation/BugsBunny>,
        <http://dbtropes.org/resource/Main/GodfreyHoNinjaMovies>,
        <http://dbtropes.org/resource/Film/Saw>,
        <http://dbtropes.org/resource/Film/FinalDestination>,
        <http://dbtropes.org/resource/Film/NightOfTheLivingDead>,
        <http://dbtropes.org/resource/Franchise/ThePhantomOfTheOpera>,
        <http://dbtropes.org/resource/Film/CarryOn>,
        <http://dbtropes.org/resource/Film/OlsenBanden>,
        <http://dbtropes.org/resource/Film/BringItOn>,
        <http://dbtropes.org/resource/Franchise/TheCrow>,
        <http://dbtropes.org/resource/Main/FuManchu>,
        <http://dbtropes.org/resource/Literature/ThePrisonerOfZenda>,
        <http://dbtropes.org/resource/Film/Rocky>,
        <http://dbtropes.org/resource/WesternAnimation/DaffyDuck>,
        <http://dbtropes.org/resource/Film/TheThinMan>,
        <http://dbtropes.org/resource/Franchise/DCCinematicUniverse>,
        <http://dbtropes.org/resource/Franchise/CharlieChan>,
        <http://dbtropes.org/resource/Main/Frankenstein>,
        <http://dbtropes.org/resource/Film/TheLittleRascals>,
        <http://dbtropes.org/resource/WesternAnimation/CasperTheFriendlyGhost>,
        <http://dbtropes.org/resource/Franchise/ChildrenOfTheCorn>,
        <http://dbtropes.org/resource/Franchise/CarryOn>,
        <http://dbtropes.org/resource/Franchise/Shrek>,
        <http://dbtropes.org/resource/Film/Taxi>,
        <http://dbtropes.org/resource/Film/RoadTo>,
        <http://dbtropes.org/resource/Main/ChildrenOfTheCorn>,
        <http://dbtropes.org/resource/Film/Flodder>,
        <http://dbtropes.org/resource/Film/Zombi2>,
        <http://dbtropes.org/resource/Franchise/Frankenstein>,
        <http://dbtropes.org/resource/Franchise/FuManchu>,
        <http://dbtropes.org/resource/Franchise/Tarzan>,
        <http://dbtropes.org/resource/Film/LeGendarmeDeSaintTropez>,
        <http://dbtropes.org/resource/Main/Mondo>,
        <http://dbtropes.org/resource/Main/Poltergeist>,
        <http://dbtropes.org/resource/Film/IlsaSheWolfOfTheSS>,
        <http://dbtropes.org/resource/Film/AndyHardy>,
        <http://dbtropes.org/resource/Film/Subspecies>,
        <http://dbtropes.org/resource/Film/TheAdventuresOfAntoineDoinel>,
        <http://dbtropes.org/resource/Main/TalesForAll>,
        <http://dbtropes.org/resource/Main/Flodder>,
        <http://dbtropes.org/resource/Main/TheAdventuresOfAntoineDoinel>,
        <http://dbtropes.org/resource/Main/Olsen-Banden>,
        <http://dbtropes.org/resource/Film/DieWildenKerl>
    ))
}

ORDER BY $trope