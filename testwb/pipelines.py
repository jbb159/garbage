# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
client = MongoClient()
collection = client["wb"]["3333333"]
from testwb.items import  wbItem



class wbPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,wbItem):
            print(item)
            collection.insert(dict(item))
        return item


