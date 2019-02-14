BOT_NAME = 'signal_dome'

SPIDER_MODULES = ['signal_dome.spiders']
NEWSPIDER_MODULE = 'signal_dome.spiders'


EXTENSIONS = {'signal_dome.extensions.HooksasyncExtension': 100}
DOWNLOADER_MIDDLEWARES = {
    'signal_dome.extensions.HooksasyncDownloaderMiddleware': 100
}

SPIDER_MIDDLEWARES = {'signal_dome.extensions.HooksasyncSpiderMiddleware': 100}
ITEM_PIPELINES = {'signal_dome.extensions.HooksasyncPipeline': 100}

# Disable S3
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
