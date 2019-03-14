# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DajiecrawlItem(scrapy.Item):
    # 岗位
    workName = scrapy.Field()
    # 薪水
    workSalary = scrapy.Field()
    # 工作要求
    workDescription = scrapy.Field()
    # 其他相似职位链接
    WorksUrl = scrapy.Field()
