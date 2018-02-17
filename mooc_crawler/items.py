# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from enum import Enum

import scrapy


class MoocCrawlerItemType(Enum):
    MOOC_COURSE = 1
    MOOC_COMMIT = 2


class MoocCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item = scrapy.Field()
    item_type = scrapy.Field()
