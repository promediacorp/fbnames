# Scrapy settings for fbnames project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fbnames'

SPIDER_MODULES = ['fbnames.spiders']
NEWSPIDER_MODULE = 'fbnames.spiders'

DOWNLOAD_DELAY = .5
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# COOKIES_DEBUG = True
DUPEFILTER_CLASS = 'fbnames.dontdedupe.FBDupeFilter'
DOWNLOADER_MIDDLEWARES = {
  'fbnames.rotateproxymiddleware.RotateProxyMiddleware': 900
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fbnames (+http://www.yourdomain.com)'
