# a test script
import re
import scrapy


class IMoocSpider(scrapy.Spider):
    name = "try-to-debug-comment-page"
    # course_id = None
    # course_name = None

    def start_requests(self):

        url = 'https://www.imooc.com/course/comment/id/783?page=1'
        yield scrapy.Request(url=url, callback=self.parse_comment_page)

    def parse_comment_page(self, response):

        course_id = response.xpath('//div[@class="course-infos"]/div[@class="w pr"]/div[@class="path"]/a[contains(@href, "learn")]/@href').extract_first()
        print('course id ----->', course_id)
        course_name = response.xpath('//div[@class="course_infos"]/div[@class="path"]/a[contains(@href, "learn")]/span/text()').extract_first()
        reg = r"/learn/(.*)"
        course_id = re.findall(reg, course_id)[0]

        for comment in response.css('ul.mod-post li.post-row'):
            user_name = comment.xpath('.//div[@class="bd"]/div[@class="tit"]/a/text()').extract_first()
            comment_content = comment.xpath('.//div[@class="bd"]/p[@class="cnt"]/text()').extract_first()
            create_time = comment.xpath('.//div[@class="bd"]/div[@class="footer clearfix"]/span[@class="l timeago"]/text()').extract_first()
            print('============================', user_name)

            yield {
                'userName': user_name,
                'commentContent': comment_content,
                'createTime': create_time,
                'courseId': course_id,
                'courseName': course_name,
            }




