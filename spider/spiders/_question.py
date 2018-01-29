import scrapy
from scrapy.conf import settings
from ..items import queItem

class UserSpider(scrapy.Spider):
    name = "que"

    def __init__(self):
        self.item = queItem()

    def start_requests(self):
        urls = [
            'https://segmentfault.com/questions/hottest/monthly?page=1',
            'https://segmentfault.com/questions/hottest/monthly?page=2',
            'https://segmentfault.com/questions/hottest/monthly?page=3',
            'https://segmentfault.com/questions/hottest/monthly?page=5',
            'https://segmentfault.com/questions/hottest/monthly?page=6',
            'https://segmentfault.com/questions/hottest/monthly?page=7',
            'https://segmentfault.com/questions/hottest/monthly?page=8',
            'https://segmentfault.com/questions/hottest/monthly?page=9'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for que in response.css('.stream-list__item'):

            self.item['title'] = que.css('.title a::text').extract_first().strip()
            self.item['answer_num'] = que.css('.answers::text').extract_first().strip()
            self.item['author'] = que.css('.author a::text').extract_first().strip()
            self.item['tags'] = que.css('.tagPopup .tag::text').extract()
            self.item['time'] = '1280977330000'
            
            url = "https://segmentfault.com" + que.css('.title a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parseC)

    def parseC(self, response):

        self.item['dec'] = response.css('.post-offset .question').extract_first().strip()
        self.item['answer'] = response.css('.post-offset .answer').extract()
        yield self.item