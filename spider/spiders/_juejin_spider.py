import scrapy
import json
from pymongo import MongoClient
from ..items import juejinItem


class JuejinSpider(scrapy.Spider):
    name = "juejin"

    def __init__(self):
        self.item = juejinItem()

    def start_requests(self):
        urls = [
            'https://juejin.im/subscribe/all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('.item .tag').re(r'st:state[=\'\"\s]+([^\'\"]*)[\'\"]?[\s\S]*'):
                tag_url = "https://timeline-merger-ms.juejin.im/v1/get_tag_entry?src=web&tagId="+ quote +"&page=1&pageSize=1&sort=rankIndex"
                yield scrapy.Request(url=tag_url, callback=self.parse_c)


    def parse_c(self, response):

        sites = json.loads(response.body_as_unicode()) 
            self.item['dec'] = sites['d']['entrylist'][0]['content']
            self.item['time'] = sites['d']['entrylist'][0]['createdAt']
            self.item['utime'] = sites['d']['entrylist'][0]['updatedAt']
            self.item['title'] = sites['d']['entrylist'][0]['title']
            self.item['tag'] = sites['d']['entrylist'][0]['tags']

            yield scrapy.Request(url=sites['d']['entrylist'][0]['originalUrl'], callback=self.parse_s)

    def parse_s(self, response):
        self.item['content'] = response.css('.post-content-container').extract_first()
        yield item





