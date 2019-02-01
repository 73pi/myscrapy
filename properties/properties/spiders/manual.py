# -*- coding: utf-8 -*-

from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.http import Request
import datetime
import urlparse
import socket
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['web']
    start_urls = ['https://voice.hupu.com/nba']

    def parse(self, response):
        # Get the next index URLs and yield Requests
        # scrapy处理请求时后入先出（LIFO）的
        # 打开调试模式，发现 [scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to ...，原来是二次解析的域名被过滤掉了
        # 解决办法:在 Request 请求参数中，设置 dont_filter = True ,Request 中请求的 URL 将不通过 allowed_domains 过滤。
        # '//*[@class="page-btn-prev"]//@href'下一页按钮的链接
        next_selector = response.xpath('//*[@class="page-btn-prev"]//@href').extract()
        for url in next_selector:
            yield Request(urlparse.urljoin(response.url, url),dont_filter=True)

        # Get item URLs and yield Requests.
        # '/html/body/div[3]/div[1]/div[2]/ul/li/div[1]/h4/a/@href'每个新闻页
        item_selector = response.xpath('/html/body/div[3]/div[1]/div[2]/ul/li/div[1]/h4/a/@href').extract()
        for url in item_selector:
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          dont_filter=True)

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

        return l.load_item()
