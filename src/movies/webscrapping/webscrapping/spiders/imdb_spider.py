import scrapy

from movies.webscrapping.webscrapping.items import MovieItem


class imdbSpider(scrapy.Spider):

    name = "imdb"
    allowed_domaines = ["imdb.com"]
    start_urls = df["movie_imdb_link"].sample(1000).tolist()

    def parse(self, response):

        for wrapper in response.css("div#pagecontent.pagecontent"):

            item = MovieItem()

            item["original_title"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//div[@class="originalTitle"]/text()'
                )
                .get(default="")
                .strip()
            )

            item["duration"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//div[@class="subtext"]/time/text()'
                )
                .get(default="")
                .strip()
            )

            item["release"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//div[@class="subtext"]/a[@title="See more release dates"]/text()'
                )
                .get(default="")
                .strip()
            )

            item["storyline"] = (
                wrapper.xpath(
                    """string(//*[@id="titleStoryLine"]//h2[contains(text(),"Storyline")]
                    /following-sibling::div[1]/p/span)"""
                )
                .get(default="")
                .strip()
            )

            item["stars"] = (
                wrapper.xpath(
                    """//*[@id="title-overview-widget"]//h4[contains(text(), "Stars:")]
                    //following-sibling::a[position() < 4]/text()"""
                ).getall()
                or ""
            )

            item["creator"] = (
                wrapper.xpath(
                    """//*[@id="title-overview-widget"]//h4[contains(text(), "Creator")]
                    //following-sibling::a[position() < 3]//text()"""
                ).getall()
                or ""
            )

            item["genres"] = (
                wrapper.xpath(
                    '//*[@id="titleStoryLine"]//h4[contains(text(),"Genres:")]//following-sibling::a/text()'
                ).getall()
                or ""
            )

            item["plot_keywords"] = (
                wrapper.xpath(
                    """//*[@id="titleStoryLine"]//h4[contains(text(),"Plot Keywords:")]
                    //following-sibling::a//span/text()"""
                ).getall()
                or ""
            )

            item["certificate"] = (
                wrapper.xpath(
                    """
                //*[@id="titleStoryLine"]//h4[contains(text(),"Certificate:")]/following-sibling::span/text()
                |
                //*[@id="title-overview-widget"]//div[@class="subtext"]/text()
                """
                )
                .get()
                .strip()
                or "Not rated"
            )

            item["movie_title"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//div[@class="title_wrapper"]/h1/text()'
                )
                .get(default="")
                .strip()
            )

            item["title_year"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//div[@class="title_wrapper"]//span[@id="titleYear"]/a/text()'
                )
                .get(default="")
                .strip()
            )

            item["imdb_score"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//span[@itemprop="ratingValue"]/text()'
                )
                .get(default="")
                .strip()
            )

            item["number_ratings"] = (
                wrapper.xpath(
                    '//*[@id="title-overview-widget"]//span[@itemprop="ratingCount"]/text()'
                )
                .get(default="")
                .strip()
            )

            item["director"] = (
                wrapper.xpath(
                    """//*[@id="title-overview-widget"]//h4[contains(text(), "Director")]
                    //following-sibling::a[position() < 3]//text()"""
                ).getall()
                or ""
            )

            item["writer"] = (
                wrapper.xpath(
                    """//*[@id="title-overview-widget"]//h4[contains(text(), "Writer")]
                    //following-sibling::a[position() < 3]//text()"""
                ).getall()
                or ""
            )

            item["episode_count"] = (
                wrapper.xpath(
                    """//*[@id="title-overview-widget"]//a[@class="bp_item np_episode_guide np_right_arrow"]
                    //span[@class="bp_sub_heading"]/text()"""
                )
                .get(default="")
                .strip()
            )

            item["country"] = (
                wrapper.xpath(
                    '//*[@id="titleDetails"]//h4[contains(text(), "Country:")]/following-sibling::a/text()'
                ).getall()
                or ""
            )

            item["budget"] = (
                wrapper.xpath(
                    '//*[@id="titleDetails"]//h4[contains(text(), "Budget:")]/following-sibling::text()'
                )
                .get(default="")
                .strip()
            )

            item["cum_worldwide_gross"] = (
                wrapper.xpath(
                    """//*[@id="titleDetails"]//h4[contains(text(), "Cumulative Worldwide Gross:")]
                    /following-sibling::text()"""
                )
                .get(default="")
                .strip()
            )

            yield
