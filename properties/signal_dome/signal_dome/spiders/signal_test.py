# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.item import Item, Field


class HooksasyncItem(Item):
    name = Field()


class TestSpider(Spider):
    name = "signal_test"
    allowed_domains = ["hupu.com"]
    start_urls = ('http://www.hupu.com',)

    def parse(self, response):
        for i in range(2):
            item = HooksasyncItem()
            item['name'] = "Hello %d" % i
            yield item
        #raise Exception("dead")
