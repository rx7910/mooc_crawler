# a sample proj to crawl imooc comments
import re
import scrapy


class IMoocSpider(scrapy.Spider):
    name = "imooc"
    course_id = None
    course_name = None

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

            print('%%%%%%%%%%%%%%%%%%%', course_id)

            self.course_id = course_id
            self.course_name = course_card.xpath("//div[@class='course-card-content']/h3/text()").extract_first()

            if course_id is not None:
                comment_url = 'https://www.imooc.com/comment/' + course_id
                print('***************************************')
                yield scrapy.Request(url=comment_url, callback=self.parse_comment_page)

        next_page = response.xpath("//div[@class='page']/a[contains(., '下一页')]/@href").extract_first()

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield response.follow(next_page, callback=self.parse)

    def parse_comment_page(self, response):
        print('***********bg**********', response.xpath("//*[@class='bd']/div"))
        for comment in response.xpath("//*[@class='bd']/div"):
            user_name = comment.xpath("//div[@class='tit']/a/text()").extract_first()
            comment_content = comment.xpath("//p[@class='cnt']/text()").extract_first()
            create_time = comment.xpath("//span[@class='l timeago']/text()").extract_first()
            # print('## user_name -----', user_name, ' ## comment -----', comment_content, '## create_time ------', create_time)
            print('============================', user_name)

            yield {
                'userName': user_name,
                'commentContent': comment_content,
                'createTime': create_time,
                'courseId': self.course_id,
                'courseName': self.course_name,
            }




