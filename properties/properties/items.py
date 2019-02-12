# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PropertiesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Primary fields
    title = Field()
    toptitle = Field()
    topnews = Field()
    news = Field()
    comeFrom = Field()

    # Calculated fields
    images = Field()
    location = Field()
    image_urls = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
