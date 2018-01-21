import scrapy
from scrapy.selector import Selector
import json
from ..items import juejinItem


class JuejinSpider(scrapy.Spider):
    name = "juejin"

    def __init__(self):
        self.item = juejinItem()

    def start_requests(self):
        
        fo = open("juejin.tpl", "r+")
        str = fo.read()
        for quote in Selector(text=str).css('.item .tag').re(r'st:state[=\'\"\s]+([^\'\"]*)[\'\"]?[\s\S]*'):
            tag_url = "https://timeline-merger-ms.juejin.im/v1/get_tag_entry?src=web&tagId="+ quote +"&page=1&pageSize=10&sort=rankIndex"
            yield scrapy.Request(url=tag_url, callback=self.parse_c)



    def parse_c(self, response):
        
        sites = json.loads(response.body_as_unicode())
        for article in  sites['d']['entrylist']:
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
        self.item['content'] = response.css('.post-content-container').extract_first()
        yield self.item





