# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):

    original_title = scrapy.Field()
    duration = scrapy.Field()
    release = scrapy.Field()
    storyline = scrapy.Field()
    stars = scrapy.Field()
    creator = scrapy.Field()
    genres = scrapy.Field()
    plot_keywords = scrapy.Field()
    certificate = scrapy.Field()
    movie_title = scrapy.Field()
    title_year = scrapy.Field()
    imdb_score = scrapy.Field()
    number_ratings = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    episode_count = scrapy.Field()
    country = scrapy.Field()
    budget = scrapy.Field()
    cum_worldwide_gross = scrapy.Field()
