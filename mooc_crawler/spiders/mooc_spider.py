# this is just a test

import re
import json

import scrapy


class MoocSpider(scrapy.Spider):
    name = "mooc"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        urls = []
        for i in range(1, 62, 1):
            urls.append('https://www.icourse163.org/category/all#?type=30&orderBy=0&pageIndex=%s' % i)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Save file %s' % filename)

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)  # shortcut

        # for a in response.css('li.next a'):
        #     yield response.follow(a, callback=self.parse)


