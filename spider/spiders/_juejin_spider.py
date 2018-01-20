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
        sites = json.loads(response.body_as_unicode()) 
        with open(filename, 'ab+') as f:
            f.write(sites['d']['entrylist'][0]['originalUrl']+'\n\n\n')
            f.write(sites['d']['entrylist'][0]['content'].encode("UTF-8")+'\n\n\n')
            f.write(sites['d']['entrylist'][0]['createdAt']+'\n\n\n')
            f.write(sites['d']['entrylist'][0]['updatedAt']+'\n\n\n')
            f.write(sites['d']['entrylist'][0]['title'].encode("UTF-8")+'\n\n\n')
            
            for tag in sites['d']['entrylist'][0]['tags']:
                f.write(tag['title'].encode("UTF-8")+'\n')
                f.write(tag['id'].encode("UTF-8")+'\n')

            yield scrapy.Request(url=sites['d']['entrylist'][0]['originalUrl'], callback=self.parse_s)

    def parse_s(self, response):
        
        filename = 'content.html'
        print response.css('.juejin-image-viewer__container')[0]+'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        with open(filename, 'wb') as f:
            f.write(response.css('.juejin-image-viewer__container').extract()[0].encode("UTF-8"))
