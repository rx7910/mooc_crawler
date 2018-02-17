# example proj in scrapy document

import scrapy


class IMoocSpider(scrapy.Spider):
    name = "imooc"

    def start_requests(self):
        urls = [
            'https://www.imooc.com/course/list?page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for course_card in response.css('a.course-card'):
            # print('course card ======', course_card)
            href_string = course_card.css('::attr(href)').re(r'\/learn\/(.*)\/').extract_first()
            # print('href_string ======', href_string)
            yield {
                'course_url': href_string,
            }

        next_page = response.xpath("//div[@class='page']/a[contains(., '下一页')]/@href").extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)


