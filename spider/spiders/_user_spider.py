import scrapy
from ..items import userItem

class UserSpider(scrapy.Spider):
    name = "user"

    def start_requests(self):
    
        maxLen = 0;

        while maxLen < 500:
            maxLen+=1
            url = 'https://www.proginn.com/' + str( maxLen )
            yield scrapy.Request(url=url, callback=self.parse_list)

        
    def parse_list(self, response):

        userlist = response.css('.user-info .title a::attr(href)')

        for userUrl in userlist:
            if userUrl.extract() != '/hire/fast':    
                yield scrapy.Request(url=userUrl.extract(), callback=self.parse)

        

    def parse(self, response):
        
        item = userItem()

        #avatar url
        item['avatar'] = response.css('.avatar .image img::attr(src)').extract_first()

        #user name
        item['name'] = response.css('.avatar .image img::attr(alt)').extract_first()

        #user address & tag
        item['address'] = response.xpath("//title/text()").extract_first()

        #user work-price
        item['work_price'] = response.css('.work-price .price::text').extract_first()

        #user work-time
        item['work_time'] = response.css('.hire-info p::text')[2].extract()

        #user dec
        dec = response.css('.panel>.content p::text')
        item['dec'] = ''
        if dec:
            item['dec'] = dec.extract_first()        
        
        #user worklist
        if len( response.css('.J_Works') ) >= 1:
            worklist = response.css('.J_Works')[0].css('li')
            workdata = []
            for work in worklist:
                workdata.append({
                    'time': work.css('.title span::text').extract_first(),
                    'cname': work.css('.title span::text')[1].extract(),
                    'job': work.css('.title span::text')[2].extract(),
                    'dec': work.css('.summary::text').extract_first()
                    })
        item['work_list'] = workdata

        #user edulist
        if len( response.css('.J_Works') ) == 2:
            edulist = response.css('.J_Works')[1].css('li')
            edudata = []
            for edu in edulist:
                edudata.append({
                    'time': edu.css('.title span::text').extract_first(),
                    'school': edu.css('.title span::text')[1].extract(),
                    'professional': edu.css('.title span::text')[2].extract(),
                    'level': edu.css('.title span::text')[3].extract(),
                    'dec': edu.css('.summary::text').extract_first()
                    })
        item['edu_list'] = edudata

        #user skilllist
        skilllist = response.css('.skill-list .skill')
        skilldata = []
        for skill in skilllist:
            skilldata.append({
                'name': skill.css('.name::text').extract_first().strip(),
                'level': skill.css('.progress div::attr(class)').extract_first()[-1]
                })
        item['skill_list'] = skilldata

        #user works
        if response.css('.works .work'):
            userwork = response.css('.works .work')
            works = []
            for work in userwork:
                works.append({
                    'name': work.css('.title a::text').extract_first(),
                    'dec': work.css('.description::text').extract_first().strip(),
                    'imgs': work.css('.J_ImgPop::attr(href)').extract()
                    })
        item['works'] = works

        yield item