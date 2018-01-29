import scrapy
from scrapy.conf import settings

class UserSpider(scrapy.Spider):
    name = "segmentfault"

    def __init__(self):
        self.sfTag = []

    def start_requests(self):
        urls = 'https://segmentfault.com/tags'
        yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        filename = 'segmentfault.html'
        with open(filename, 'ab+') as f:
            for tag in response.css('.tagPopup'):
                tagName = tag.css('.tag::attr(data-original-title)')[0].extract().strip()
                iurl = "https://segmentfault.com/t/" + tagName
                
                if tagName not in self.sfTag:
                    self.sfTag.append(tagName)
                    f.write("https://segmentfault.com/t/" + tagName.encode("UTF-8")+'\n\n')