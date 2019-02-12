# -*- coding: utf-8 -*-

from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.http import Request
import urlparse
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['hupu.com']
    start_urls = ['https://voice.hupu.com/nba']

    def parse(self, response):
        # Get the next index URLs and yield Requests
        # scrapy处理请求时后入先出（LIFO）的
        # 打开调试模式，发现 [scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to ...，原来是二次解析的域名被过滤掉了(主要是与allowed_domains冲突了)
        # 解决办法:在 Request 请求参数中，设置 dont_filter = True ,Request 中请求的 URL 将不通过 allowed_domains 过滤。
        # '//*[@class="page-btn-prev"]//@href'下一页按钮的链接
        next_selector = response.xpath('//*[@class="page-btn-prev"]//@href').extract()
        for url in next_selector:
            yield Request(urlparse.urljoin(response.url, url))

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

        # image
        l.add_xpath('image_urls', '//*[@class="artical-importantPic"][1]/img/@src',
                    MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        return l.load_item()
