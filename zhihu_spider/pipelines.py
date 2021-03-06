# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy import log

class ZhihuSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USERNAME'],
            password=settings['MONGODB_PWD'],
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        
        self.collection.insert(dict(item))
        log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        
        return item

class MongoDBDaily(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USERNAME'],
            password=settings['MONGODB_PWD'],
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_ZHIHU_DAILY']]

    def process_item(self, item, spider):
        
        self.collection.insert(dict(item))
        log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        
        return item