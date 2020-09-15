from scrapy.crawler import CrawlerProcess
import os
import time

from movies.webscrapping.spiders.imdb_spider import ImdbSpider


if __name__ == "__main__":

    start_time = time.time()

    os.system("rm movies.json")
    process = CrawlerProcess()
    process.crawl(ImdbSpider)
    process.start()

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))
