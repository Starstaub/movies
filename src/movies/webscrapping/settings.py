BOT_NAME = 'webscrapping'

SPIDER_MODULES = ['webscrapping.spiders']
NEWSPIDER_MODULE = 'webscrapping.spiders'

OBOTSTXT_OBEY = True

ITEM_PIPELINES = {'webscrapping.pipelines.MongoDBPipeline': 300, }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "movies"
MONGODB_COLLECTION = "movie_data"
