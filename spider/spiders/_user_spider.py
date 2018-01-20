import scrapy
import _db_

class UserSpider(scrapy.Spider):
    name = "user"

    def start_requests(self):
    
        maxLen = 0;

        while maxLen < 500:
            maxLen+=1
            url = 'https://www.proginn.com/' + str( maxLen )
            yield scrapy.Request(url=url, callback=self.parse_list)

        
    def parse_list(self, response):
        page = response.url.split("/")[-2]
        filename = 'user-list.html'

        userlist = response.css('.user-info .title a::attr(href)')

        for userUrl in userlist:
            if userUrl.extract() != '/hire/fast':
                with open(filename, 'ab+') as f:
                    f.write(userUrl.extract().encode("UTF-8")+'\n\n')
                    yield scrapy.Request(url=userUrl.extract(), callback=self.parse)

        

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'user-data.html'
        with open(filename, 'ab+') as f:
            
            coll = _db_.get_db().people
            #avatar url
            f.write('<hr/>'+response.css('.avatar .image img::attr(src)').extract_first().encode("UTF-8")+'\n\n')

            #user name
            f.write(response.css('.avatar .image img::attr(alt)').extract_first().encode("UTF-8")+'\n\n')
            
            #user address & tag
            f.write(response.xpath("//title/text()").extract_first().encode("UTF-8")+'\n\n')

            #user work-price
            f.write(response.css('.work-price .price::text').extract_first().encode("UTF-8")+'\n\n')
            
            #user work-time
            f.write(response.css('.hire-info p::text')[2].extract().encode("UTF-8")+'\n\n')
            
            #user dec
            dec = response.css('.panel>.content p::text')
            if dec:
                f.write(dec.extract_first().encode("UTF-8")+'\n\n')
            
            
            
            #user worklist
            if len( response.css('.J_Works') ) >= 1:
                worklist = response.css('.J_Works')[0].css('li')

                for work in worklist:
                    f.write(work.css('.title span::text').extract_first().encode("UTF-8")+'\n\n')
                    f.write(work.css('.title span::text')[1].extract().encode("UTF-8")+'\n\n')
                    f.write(work.css('.title span::text')[2].extract().encode("UTF-8")+'\n\n')
                    f.write(work.css('.summary::text').extract_first().encode("UTF-8")+'\n\n')
                
            #user edulist
            if len( response.css('.J_Works') ) >= 2:
                edulist = response.css('.J_Works')[1].css('li')

                for edu in edulist:
                    f.write(edu.css('.title span::text').extract_first().encode("UTF-8")+'\n\n')
                    f.write(edu.css('.title span::text')[1].extract().encode("UTF-8")+'\n\n')
                    f.write(edu.css('.title span::text')[2].extract().encode("UTF-8")+'\n\n')
                    f.write(edu.css('.summary::text').extract_first().encode("UTF-8")+'\n\n')
     
            #user skilllist
            skilllist = response.css('.skill-list .skill')

            for skill in skilllist:
                f.write(skill.css('.name::text').extract_first().strip().encode("UTF-8")+'\n\n')
                f.write(skill.css('.progress div::attr(class)').extract_first().encode("UTF-8")+'\n\n')

            #user works
            if response.css('.works .work'):
                userwork = response.css('.works .work')

                for work in userwork:
                    f.write(work.css('.title a::text').extract_first().encode("UTF-8")+'\n\n')
                    f.write(work.css('.description::text').extract_first().strip().encode("UTF-8")+'\n\n')

                    coll.insert({'url' : work.css('.J_ImgPop::attr(href)').extract()})

                    for workimg in work.css('.J_ImgPop::attr(href)'):
                        f.write(workimg.extract().strip().encode("UTF-8")+'\n\n')
