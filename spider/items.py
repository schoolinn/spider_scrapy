# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class userItem(scrapy.Item):
    name = scrapy.Field()
    avatar = scrapy.Field()
    dec = scrapy.Field()
    work_time = scrapy.Field()
    work_price = scrapy.Field()
    address = scrapy.Field()
    work_list = scrapy.Field()
    edu_list = scrapy.Field()
    skill_list = scrapy.Field()
    works = scrapy.Field()


class juejinItem(scrapy.Item):
    objectId = scrapy.Field()
    title = scrapy.Field()
    dec = scrapy.Field()
    time = scrapy.Field()
    utime = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()

class queItem(scrapy.Item):
    title = scrapy.Field()
    answer_num = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    time = scrapy.Field()
    dec = scrapy.Field()
    answer = scrapy.Field()