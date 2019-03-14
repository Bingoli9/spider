# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pymongo
from DajieCrawl.items import DajieWorkListItem

class DajiecrawlPipeline(object):
    def __init__(self, mongo_uri, mongo_db,replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'dajie'),
            replicaset = crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        if isinstance(item,YunqiBookListItem):
            self._process_booklist_item(item)
        else:
            self._process_bookeDetail_item(item)
        return item



    def _process_worklist_item(self,item):
        '''
        处理岗位
        :param item:
        :return:
        '''
        self.db.workInfo.insert(dict(item))
