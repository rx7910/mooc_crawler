# example proj in scrapy document

import scrapy


class IMoocSpider(scrapy.Spider):
    name = "imooc"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for course_card in response.css('a.course-card'):
            print('course card ======', course_card)
            href_string = course_card.css('::attr(href)').extract()
            print('href_string ======', href_string)
            yield href_string

        next_page = response.xpath("//div[@class='page']/a[contains(., '下一页')]/a/@href")

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)


