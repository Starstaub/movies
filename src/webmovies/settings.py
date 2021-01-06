BOT_NAME = 'webmovies'

USER_AGENT = "webmovies"

SPIDER_MODULES = ['webmovies.spiders']
NEWSPIDER_MODULE = 'webmovies.spiders'

OBOTSTXT_OBEY = True

ITEM_PIPELINES = {'webmovies.pipelines.MongoDBPipeline': 300, }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "movies"
MONGODB_COLLECTION = "data"

CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 0.5
