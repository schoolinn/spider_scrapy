import scrapy
from scrapy.selector import Selector
import json
import os
from ..items import juejinItem


class JuejinSpider(scrapy.Spider):
    name = "juejin"

    def __init__(self):
        self.item = juejinItem()

    def start_requests(self):
        
        fo = open(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"/juejin.tpl", "r+")
        str = fo.read()
        fo.close()
        for quote in Selector(text=str).css('.item .tag').re(r'st:state[=\'\"\s]+([^\'\"]*)[\'\"]?[\s\S]*'):
            tag_url = "https://timeline-merger-ms.juejin.im/v1/get_tag_entry?src=web&tagId="+ quote +"&page=1&pageSize=50&sort=rankIndex"
            yield scrapy.Request(url=tag_url, callback=self.parse_c)



    def parse_c(self, response):
        
        sites = json.loads(response.body_as_unicode())
        for article in  sites['d']['entrylist']:
            self.item['objectId'] = article['objectId']
            self.item['dec'] = article['content']
            self.item['time'] = article['createdAt']
            self.item['utime'] = article['updatedAt']
            self.item['title'] = article['title']

            tags = []
            for tag in article['tags']:
                tags.append({
                    'name': tag['title'],
                    'id': tag['id']
                    })
            self.item['tag'] = tags

            yield scrapy.Request(url=article['originalUrl'], callback=self.parse_s)

    def parse_s(self, response):
        content = response.css('.post-content-container').extract_first()
        if content:
            self.item['content'] = content
        yield self.item





