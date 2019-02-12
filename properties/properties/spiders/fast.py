# -*- coding: utf-8 -*-

from properties.items import PropertiesItem
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.http import Request
import urlparse
import scrapy

#快速在索引查找信息,并且索引页也只是CLOSESPIDER_PAGECOUNT-1页
class BasicSpider(scrapy.Spider):
    name = 'fast'
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

        # iterate through products and create PropertiesItems.
        # ''//*[@class="list-hd"]'每个新闻页selector
        selectors = response.xpath('//*[@class="list-hd"]')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), selector=selector)

        #load fields using XPath expressions
        #加'.'是相对地址的
        # '/html/body/div[4]/div[1]/div[1]/h1/text()'新闻标题
        l.add_xpath(
            'title',
            './/a/text()',
            MapCompose(unicode.strip, unicode.title))

        # Housekeeping fields
        make_url = lambda i: urlparse.urljoin(response.url, i)
        l.add_xpath('url', './/a/@href', MapCompose(make_url))

        return l.load_item()
