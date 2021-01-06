from scrapy import Item, Field


class MovieItem(Item):  # pylint: disable=too-many-ancestors

    original_title = Field()
    duration = Field()
    release = Field()
    storyline = Field()
    stars = Field()
    creator = Field()
    genres = Field()
    plot_keywords = Field()
    certificate = Field()
    movie_title = Field()
    title_year = Field()
    imdb_score = Field()
    number_ratings = Field()
    director = Field()
    writer = Field()
    episode_count = Field()
    country = Field()
    budget = Field()
    cum_worldwide_gross = Field()
    poster = Field()
    big_poster = Field()
