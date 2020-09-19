import pandas as pd
from scrapy import Spider

from ..items import MovieItem


class ImdbSpider(Spider):

    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = pd.read_csv(
        "/Users/mary/git/movies/src/movies/movie_urls.csv"
    )["movie_imdb_link"][:3].tolist()

    def parse(self, response):

        for wrapper in response.css("div#pagecontent.pagecontent"):

            movie = MovieItem()

            movie["original_title"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//div[@class="originalTitle"]/text()'
            ).get(default="").strip()

            movie["duration"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//div[@class="subtext"]/time/text()'
            ).get(default="").strip()

            movie["release"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//div[@class="subtext"]/a[@title="See more release dates"]/text()'
            ).get(default="").strip()

            movie["storyline"] = wrapper.xpath(
                """string(//*[@id="titleStoryLine"]//h2[contains(text(),"Storyline")]
                /following-sibling::div[1]/p/span)"""
            ).get(default="").strip()

            movie["stars"] = wrapper.xpath(
                """//*[@id="title-overview-widget"]//h4[contains(text(), "Stars:")]
                //following-sibling::a[position() < 4]/text()"""
            ).getall() or ""

            movie["creator"] = wrapper.xpath(
                """//*[@id="title-overview-widget"]//h4[contains(text(), "Creator")]
                //following-sibling::a[position() < 3]//text()"""
            ).getall() or ""

            movie["genres"] = wrapper.xpath(
                '//*[@id="titleStoryLine"]//h4[contains(text(),"Genres:")]//following-sibling::a/text()'
            ).getall() or ""

            movie["plot_keywords"] = wrapper.xpath(
                """//*[@id="titleStoryLine"]//h4[contains(text(),"Plot Keywords:")]
                //following-sibling::a//span/text()"""
            ).getall() or ""

            movie["certificate"] = wrapper.xpath(
                """
                //*[@id="titleStoryLine"]//h4[contains(text(),"Certificate:")]/following-sibling::span/text()
                |
                //*[@id="title-overview-widget"]//div[@class="subtext"]/text()
                """
            ).get().strip() or "Not rated"

            movie["movie_title"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//div[@class="title_wrapper"]/h1/text()'
            ).get(default="").strip()

            movie["title_year"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//div[@class="title_wrapper"]//span[@id="titleYear"]/a/text()'
            ).get(default="").strip()

            movie["imdb_score"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//span[@itemprop="ratingValue"]/text()'
            ).get(default="").strip()

            movie["number_ratings"] = wrapper.xpath(
                '//*[@id="title-overview-widget"]//span[@itemprop="ratingCount"]/text()'
            ).get(default="").strip()

            movie["director"] = wrapper.xpath(
                """//*[@id="title-overview-widget"]//h4[contains(text(), "Director")]
                //following-sibling::a[position() < 3]//text()"""
            ).getall() or ""

            movie["writer"] = wrapper.xpath(
                """//*[@id="title-overview-widget"]//h4[contains(text(), "Writer")]
                //following-sibling::a[position() < 3]//text()"""
            ).getall() or ""

            movie["episode_count"] = wrapper.xpath(
                """//*[@id="title-overview-widget"]//a[@class="bp_item np_episode_guide np_right_arrow"]
                //span[@class="bp_sub_heading"]/text()"""
            ).get(default="").strip()

            movie["country"] = wrapper.xpath(
                '//*[@id="titleDetails"]//h4[contains(text(), "Country:")]/following-sibling::a/text()'
            ).getall() or ""

            movie["budget"] = wrapper.xpath(
                '//*[@id="titleDetails"]//h4[contains(text(), "Budget:")]/following-sibling::text()'
            ).get(default="").strip()

            movie["cum_worldwide_gross"] = wrapper.xpath(
                """//*[@id="titleDetails"]//h4[contains(text(), "Cumulative Worldwide Gross:")]
                /following-sibling::text()"""
            ).get(default="").strip()

            yield movie
