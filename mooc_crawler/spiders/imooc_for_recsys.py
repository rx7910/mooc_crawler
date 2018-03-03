# a sample proj to crawl imooc comments

import re
import scrapy
import datetime

class IMoocSpider(scrapy.Spider):
    name = "coursescore_for_recsys"
    # course_id = None
    # course_name = None

    def start_requests(self):
        urls = [
            'https://www.imooc.com/course/list?page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for course_card in response.css('a.course-card'):
            # print('course card ======', course_card)
            href_string = course_card.css('::attr(href)').extract_first()
            reg = r"/learn/(.*)"
            course_id = re.findall(reg, href_string)[0]

            comment_url = 'https://www.imooc.com/coursescore/' + course_id + '?page=1'
            yield scrapy.Request(url=comment_url, callback=self.parse_comment_page)

        next_page = response.xpath("//div[@class='page']/a[contains(., '下一页')]/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)

    def parse_comment_page(self, response):
        course_id = response.xpath(
            '//div[@class="course-infos"]/div[@class="w pr"]/div[@class="path"]/a[contains(@href, "learn")]/@href')\
            .extract_first()
        course_name = response.xpath(
            '//div[@class="course-infos"]/div[@class="w pr"]/div[@class="hd clearfix"]/h2/text()').extract_first()
        reg = r"/learn/(.*)"
        course_id = re.findall(reg, course_id)[0]

        category = response.xpath(
            '//div[@class="course-infos"]/div[@class="w pr"]/div[@class="path"]/a')[1].xpath('.//text()').extract_first()

        for comment in response.css('div.evaluation-list div.evaluation div.evaluation-con div.content-box'):
            user_name = comment.xpath('.//div[@class="user-info clearfix"]/a/text()').extract_first()
            user_id = re.findall(r"^/u/(.*)/courses$", comment.xpath('.//div[@class="user-info clearfix"]/a[@class="username"]/@href').extract_first())[0]
            star_count = len(comment.xpath('.//div[@class="user-info clearfix"]/div[@class="star-box"]/i[@class="icon-star2 active"]'))
            comment_content = comment.xpath('.//p/text()').extract_first()
            create_time = re.findall(r"时间：(.*)", comment.xpath('.//div[@class="info"]/span[@class="time"]/text()').extract_first())[0]
            if len(re.findall(r"天前", create_time)) > 0:
                days_ago = re.findall(r"(.*)天前", create_time)[0]
                create = datetime.datetime.now() - datetime.timedelta(days=int(days_ago))
                create_time = create.strftime("%Y-%m-%d")
            if len(re.findall(r"小时前", create_time)) > 0:
                create_time = datetime.datetime.now().strftime("%Y-%m-%d")

            if user_name is not None and user_name != '' and comment_content is not None and comment_content != '':
                yield {
                    'reviewerID': user_id,
                    'asin': course_id,
                    'reviewText': comment_content,
                    'overall': star_count
                }

        # next_comment_page = response.xpath('//div[@class="page"]/a[contains(., "下一页")]/@href').extract_first()
        # if next_comment_page is not None:
        #     next_comment_page = response.urljoin(next_comment_page)
        #     yield response.follow(next_comment_page, callback=self.parse_comment_page)




