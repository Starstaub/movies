DROP TABLE movie_data;


CREATE TABLE movie_data (

    id UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),

    original_title varchar(100),
    duration int,
    release varchar(50),
    storyline varchar(20000),
    certificate varchar(15),
    movie_title varchar(100),
    title_year int,
    imdb_score float,
    number_ratings int,
    episode_count int,
    budget int,
    cum_worldwide_gross int,

);