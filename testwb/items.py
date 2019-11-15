# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class hrItem(scrapy.Item):
    pos = scrapy.Field()
    site = scrapy.Field()


class wbItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    dianzan = scrapy.Field()
    pinglun = scrapy.Field()
    zhuanfa = scrapy.Field()
    message = scrapy.Field()