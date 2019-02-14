# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
import datetime

class EasySpider(CrawlSpider):
    name = 'easy'
    # allowed_domains改成hupu.com防止request的地址冲突
    allowed_domains = ['hupu.com']
    start_urls = ['https://voice.hupu.com/nba']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="page-btn-prev"]')),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[1]/div[2]/ul/li/div[1]/h4'),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        #load fields using XPath expressions
        # '/html/body/div[4]/div[1]/div[1]/h1/text()'新闻标题
        l.add_xpath(
            'title',
            '/html/body/div[4]/div[1]/div[1]/h1/text()',
            MapCompose(unicode.strip, unicode.title))
        # '//*[@id="source_baidu"]/a/text()'新闻来源
        l.add_xpath(
            'comeFrom',
            '//*[@id="source_baidu"]/a/text()')

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
