DROP TABLE movie_data;
DROP TABLE description_df;
DROP TABLE country_stars_df;
DROP TABLE creation_df;


CREATE TABLE movie_data (

    idx int,
    original_title varchar(100),
    duration int,
    release varchar(50),
    storyline varchar(5000),
    certificate varchar(50),
    movie_title varchar(100),
    title_year int,
    imdb_score float,
    number_ratings int,
    episode_count int,
    budget float,
    cum_worldwide_gross float,
    type varchar(50),
    kind varchar(50)

);

CREATE TABLE description_df (

    idx int,
    genres_1 varchar(20),
    genres_2 varchar(20),
    genres_3 varchar(20),
    genres_4 varchar(20),
    genres_5 varchar(20),
    genres_6 varchar(20),
    genres_7 varchar(20),
    genres_8 varchar(20),
    plot_keywords_1 varchar(50),
    plot_keywords_2 varchar(50),
    plot_keywords_3 varchar(50),
    plot_keywords_4 varchar(50),
    plot_keywords_5 varchar(50),

);

CREATE TABLE country_stars_df (

    idx int,
    stars_1 varchar(100),
    stars_2 varchar(100),
    stars_3 varchar(100),
    country_1 varchar(50),
    country_2 varchar(50),
    country_3 varchar(50),
    country_4 varchar(50),
    country_5 varchar(50),
    country_6 varchar(50),
    country_7 varchar(50),
    country_8 varchar(50),
    country_9 varchar(50),
    country_10 varchar(50),
    country_11 varchar(50),
    country_12 varchar(50),
    country_13 varchar(50),
    country_14 varchar(50),
    country_15 varchar(50),
    country_16 varchar(50),
    country_17 varchar(50),
    country_18 varchar(50),
    country_19 varchar(50),

);

CREATE TABLE creation_df (

    idx int,
    director_1 varchar(100),
    director_2 varchar(100),
    writer_1 varchar(100),
    writer_2 varchar(100),
    creator_1 varchar(100),
    creator_2 varchar(100),

);