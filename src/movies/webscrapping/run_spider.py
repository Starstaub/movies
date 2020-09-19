from scrapy.crawler import CrawlerProcess
import os
import time

from scrapy.utils.project import get_project_settings
from movies.webscrapping.spiders.imdb_spider import ImdbSpider


if __name__ == "__main__":

    start_time = time.time()

    # os.system("rm movies.json")
    process = CrawlerProcess(get_project_settings())
    process.crawl(ImdbSpider)
    process.start()

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))
