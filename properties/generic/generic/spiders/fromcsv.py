# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose


class FromcsvSpider(scrapy.Spider):
    name = 'fromcsv'

    def start_requests(self):
        # 默认打开todo.csv，也可以利用"-a file=文件名"进行指定csv文件
        # scrapy crawl fromcsv -a file=todo.csv -o out.csv
        with open(getattr(self, 'file', 'todo.csv'), 'rU') as f:
            reader = csv.DictReader(f)
            for line in reader:
                request = Request(line.pop('url'))
                # 在request.meta存储来自csv的字段名和xpath表达式
                request.meta['fields'] = line
                yield request

    def parse(self, response):
        item = Item()
        l = ItemLoader(item=item, response=response)
        for name, xpath in response.meta['fields'].iteritems():
            if xpath:
                # 动态添加新字段
                item.fields[name] = Field()
                l.add_xpath(name, xpath, MapCompose(unicode.strip, unicode.title))
        return l.load_item()
