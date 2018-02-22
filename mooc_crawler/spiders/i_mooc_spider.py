# a sample proj to crawl imooc comments
import re
import scrapy


class IMoocSpider(scrapy.Spider):
    name = "imooc"
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

            comment_url = 'https://www.imooc.com/course/comment/id/' + course_id + '?page=1'
            print('***************************************', comment_url)
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

        for comment in response.css('ul.mod-post li.post-row'):
            user_name = comment.xpath('.//div[@class="bd"]/div[@class="tit"]/a/text()').extract_first()
            comment_content = comment.xpath('.//div[@class="bd"]/p[@class="cnt"]/text()').extract_first()
            create_time = comment.xpath(
                './/div[@class="bd"]/div[@class="footer clearfix"]/span[@class="l timeago"]/text()').extract_first()
            create_time = re.findall(r"时间：(.*)", create_time)[0]

            if user_name is not None and user_name != '' and comment_content is not None and comment_content != '':
                yield {
                    'userName': user_name,
                    'commentContent': comment_content,
                    'createTime': create_time,
                    'courseId': course_id,
                    'courseName': course_name,
                }

        next_comment_page = response.xpath('//div[@class="page"]/a[contains(., "下一页")]/@href').extract_first()
        if next_comment_page is not None:
            next_comment_page = response.urljoin(next_comment_page)
            yield response.follow(next_comment_page, callback=self.parse_comment_page)




