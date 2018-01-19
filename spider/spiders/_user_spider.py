import scrapy
import _db_

class UserSpider(scrapy.Spider):
    name = "user"

    def start_requests(self):
        urls = [
            'https://www.proginn.com/wo/122308'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'user-%s.html' % page
        with open(filename, 'wb') as f:
            
            coll = _db_.get_db().people
            #coll.insert({'name': response.css('.avatar .image img::attr(alt)').extract_first(),'url':response.css('.avatar .image img::attr(src)').extract_first()})

            #avatar url
            f.write(response.css('.avatar .image img::attr(src)').extract_first().encode("UTF-8")+'\n\n')

            #user name
            f.write(response.css('.avatar .image img::attr(alt)').extract_first().encode("UTF-8")+'\n\n')
            
            #user address & tag
            f.write(response.xpath("//title/text()").extract_first().encode("UTF-8")+'\n\n')

            #user work-price
            f.write(response.css('.work-price .price::text').extract_first().encode("UTF-8")+'\n\n')
            
            #user work-time
            f.write(response.css('.hire-info p::text')[2].extract().encode("UTF-8")+'\n\n')
            
            #user dec
            f.write(response.css('.panel>.content p::text').extract_first().encode("UTF-8")+'\n\n')
            
            #user worklist
            worklist = response.css('.J_Works')[0].css('li')

            for work in worklist:
                f.write(work.css('.title span::text')[0].extract().encode("UTF-8")+'\n\n')
                f.write(work.css('.title span::text')[1].extract().encode("UTF-8")+'\n\n')
                f.write(work.css('.title span::text')[2].extract().encode("UTF-8")+'\n\n')
                f.write(work.css('.summary::text')[0].extract().encode("UTF-8")+'\n\n')
            
            #user edulist
            edulist = response.css('.J_Works')[1].css('li')

            for edu in edulist:
                f.write(edu.css('.title span::text')[0].extract().encode("UTF-8")+'\n\n')
                f.write(edu.css('.title span::text')[1].extract().encode("UTF-8")+'\n\n')
                f.write(edu.css('.title span::text')[2].extract().encode("UTF-8")+'\n\n')
                f.write(edu.css('.summary::text')[0].extract().encode("UTF-8")+'\n\n')
 
            #user skilllist
            skilllist = response.css('.skill-list .skill')

            for skill in skilllist:
                f.write(skill.css('.name::text')[0].extract().strip().encode("UTF-8")+'\n\n')
                f.write(skill.css('.progress div::attr(class)')[0].extract().encode("UTF-8")+'\n\n')

            #user works
            userwork = response.css('.works .work')

            for work in userwork:
                f.write(work.css('.title a::text')[0].extract().encode("UTF-8")+'\n\n')
                f.write(work.css('.duty::text')[0].extract().encode("UTF-8")+'\n\n')
                f.write(work.css('.description::text')[0].extract().strip().encode("UTF-8")+'\n\n')
                print work.css('.J_ImgPop::attr(href)').extract()[0]
                for workimg in work.css('.J_ImgPop::attr(href)'):
                    f.write(workimg.extract().strip().encode("UTF-8")+'\n\n')