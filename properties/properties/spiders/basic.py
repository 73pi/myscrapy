# -*- coding: utf-8 -*-
import scrapy
from properties.items import PropertiesItem

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://voice.hupu.com/nba']

    def parse(self, response):
        self.log("title: %s" % response.xpath(
            '/html/body/div[2]/div/div[1]/ul/li[3]/a/text()'
        ).extract())
        self.log("h2: %s" % response.xpath(
            '//h2/text()'
        ).extract())

        item = PropertiesItem()
        item['title'] = response.xpath(
            '/html/body/div[2]/div/div[1]/ul/li[3]/a/text()'
        ).extract()
        item['h2'] = response.xpath(
            '//h2/text()'
        ).extract()

        return item
