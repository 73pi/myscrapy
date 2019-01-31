# -*- coding: utf-8 -*-

from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
import datetime
import urlparse
import socket
import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://voice.hupu.com/nba']

    def parse(self, response):
        """This function parses a property page（contract爬虫可行测试）.
        @url https://voice.hupu.com/nba
        @returns items l
        @scrapes title toptitle topnews news
        @scrapes url project spider server date
        """
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        #load fields using XPath expressions
        l.add_xpath(
            'title',
            '/html/body/div[3]/div[1]/div[1]/h2/text()')
        l.add_xpath(
            'news',
            '/html/body/div[3]/div[1]/div[2]/ul/li/div[1]/h4/a/text()',
            MapCompose(unicode.strip, unicode.title))
        l.add_xpath(
            'toptitle',
            '//*[@class="hd"]/h2/text()')
        l.add_xpath(
            'topnews',
            '//*[@class="bd"]//a/text()')

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostbyname('nba.hupu.com'))
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

        """学习代码
        self.log("title: %s" % response.xpath(
            '//h2/text()'
        ).extract())

        item = PropertiesItem()
        item['title'] = response.xpath(
            '/html/body/div[3]/div[1]/div[1]/h2/text()'
        ).extract()
        item['news'] = response.xpath(
            '/html/body/div[3]/div[1]/div[2]/ul/li/div[1]/h4/a/text()'
        ).extract()
        item['toptitle'] = response.xpath(
            '//*[@class="hd"]/h2/text()'
        ).extract()
        item['topnews'] = response.xpath(
            '//*[@class="bd"]//a/text()'
        ).extract()
        
        return item
        """
