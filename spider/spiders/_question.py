import scrapy

class UserSpider(scrapy.Spider):
    name = "que"

    def start_requests(self):
        urls = [
            'https://segmentfault.com/questions/hottest/monthly'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        filename = 'que.html'
        with open(filename, 'wb') as f:
            for que in response.css('.stream-list__item'):
                f.write(que.extract().encode("UTF-8")+'\n\n')

                f.write(que.css('.title a::text').extract_first().encode("UTF-8")+'\n\n')
                f.write(que.css('.title a::attr(href)').extract_first().encode("UTF-8")+'\n\n')
                f.write(que.css('.author a::text').extract_first().encode("UTF-8")+'\n\n')
                f.write(que.css('.answers::text').extract_first().encode("UTF-8")+'\n\n')
                f.write(que.css('.tagPopup .tag::text').extract_first().encode("UTF-8")+'\n\n')
                url = "https://segmentfault.com" + que.css('.title a::attr(href)').extract_first()
                yield scrapy.Request(url=url, callback=self.parseC)

    def parseC(self, response):
        filename = 'que_c.html'
        with open(filename, 'ab+') as f:
            f.write(response.css('.post-offset .question').extract_first().encode("UTF-8")+'\n\n')
            f.write(response.css('.post-offset .answer').extract_first().encode("UTF-8")+'\n\n')