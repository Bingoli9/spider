# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlItem(scrapy.Item):
    filmName = scrapy.Field()

    score = scrapy.Field()
    
    area = scrapy.Field()
    
    year = scrapy.Field()
    
    kind = scrapy.Field()

    director = scrapy.Field()

    actor= scrapy.Field()
