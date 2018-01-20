import scrapy
import json
from pymongo import MongoClient


class JuejinSpider(scrapy.Spider):
    name = "juejin"

    tagList = []

    def start_requests(self):
        urls = [
            'https://juejin.im/subscribe/all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for quote in response.css('.item .tag').re(r'st:state[=\'\"\s]+([^\'\"]*)[\'\"]?[\s\S]*'):
                self.tagList.append(quote);
                #print self.tagList
                tag_url = "https://timeline-merger-ms.juejin.im/v1/get_tag_entry?src=web&tagId="+ quote +"&page=1&pageSize=1&sort=rankIndex"
                yield scrapy.Request(url=tag_url, callback=self.parse_c)


    def parse_c(self, response):
        filename = 'juejin.html'
        with open(filename, 'ab+') as f:
            f.write(response.body)

            #for quote in response.css('.item .tag').re(r'st:state[=\'\"\s]+([^\'\"]*)[\'\"]?[\s\S]*'):
                #f.write(quote+'\n\n\n')
                #print self.tagList
        sites = json.loads(response.body_as_unicode()) 
        print sites['d']['total']  
