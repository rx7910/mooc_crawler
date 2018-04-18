# a sample proj to crawl imooc comments
import re
import scrapy


class IMoocSpider(scrapy.Spider):
    name = "imooc"
    # course_id = None
    # course_name = None

    def start_requests(self):
        # define the scrapy target
        urls = [
            'https://www.imooc.com/course/list?page=1',
        ]

        # the first level to loop -> loop the target list, now we have only one target url
        for url in urls:
            # scrapy will post a http request automatically and return a http response
            # you yield the request here in this loop unit
            # give the request a url
            # and define a call back to resolve the response in the next line
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # after a response returned by the target url, this function will be called,
        # in this function , you resolve the response result, for example, you can
        # extract your target data here, you can catch http error, or you can just pass,
        # if you have a next target in current page's response ,you can also yield a new Request,
        # and git a new url and new callback fn to this Request

        # in this function, we resolve the response, extract data we need and yield a new request
        #  because we have next level's target to scarpy

        for course_card in response.css('a.course-card'):

            # in this case , i noted that, only the course id is valuable to me,
            # the real data i need is in another detail page which url contains a course id,
            # so i need to match the id out and build a new url string and go into next level's callback
            # and in the next level's callback, we extract the real data we need
            href_string = course_card.css('::attr(href)').extract_first()
            reg = r"/learn/(.*)"
            # now we get the course id
            course_id = re.findall(reg, href_string)[0]

            comment_url = 'https://www.imooc.com/course/comment/id/' + course_id + '?page=1'
            # print('***************************************', comment_url)

            # now we create a new Request, give the next level's url and dim the next level's parse-response-function
            yield scrapy.Request(url=comment_url, callback=self.parse_comment_page)

        # i have said in the upper scope, in this parse() function, we only get a page of course list,
        # we just need the course id, and the id we have used correctly before this line, so what next?
        # what if this page of course list have a next page? if we stop here, we will just scrap a page of course's data
        # so we need to tell the small spider that ' you have next page to go and just go as i told you'
        # as you can see , i extract necessary data for next url in the next line
        next_page = response.xpath("//div[@class='page']/a[contains(., '下一页')]/@href").extract_first()
        if next_page is not None:
            # i cancat the url to the domain
            next_page = response.urljoin(next_page)
            # yield the request out, i used a short cut to yield the request ,you can also new a Request and yield out,
            # this's all the same

            # the next page of course list will reuse the parse() function,
            # all next page will also go to the next' next page until there is no next page
            yield response.follow(next_page, callback=self.parse)

    def parse_comment_page(self, response):

        # this function is to resolve the real comment data for the course detail page

        # i extract the course id
        course_id = response.xpath(
            '//div[@class="course-infos"]/div[@class="w pr"]/div[@class="path"]/a[contains(@href, "learn")]/@href')\
            .extract_first()
        # i extract the course name
        course_name = response.xpath(
            '//div[@class="course-infos"]/div[@class="w pr"]/div[@class="hd clearfix"]/h2/text()').extract_first()
        reg = r"/learn/(.*)"
        course_id = re.findall(reg, course_id)[0]

        # there are a lot of comments, evert comment, i extract the target data
        for comment in response.css('ul.mod-post li.post-row'):

            # extract targte data for current comment
            user_name = comment.xpath('.//div[@class="bd"]/div[@class="tit"]/a/text()').extract_first()
            comment_content = comment.xpath('.//div[@class="bd"]/p[@class="cnt"]/text()').extract_first()
            create_time = comment.xpath(
                './/div[@class="bd"]/div[@class="footer clearfix"]/span[@class="l timeago"]/text()').extract_first()
            create_time = re.findall(r"时间：(.*)", create_time)[0]

            if user_name is not None and user_name != '' and comment_content is not None and comment_content != '':

                # if you yield a dist or string or another two data object that i forget, the
                #  scrapy will save automatically
                yield {
                    'userName': user_name,
                    'commentContent': comment_content,
                    'createTime': create_time,
                    'courseId': course_id,
                    'courseName': course_name,
                }

        # same question again , what if the current detail page's comments have next page?

        next_comment_page = response.xpath('//div[@class="page"]/a[contains(., "下一页")]/@href').extract_first()
        if next_comment_page is not None:
            next_comment_page = response.urljoin(next_comment_page)
            yield response.follow(next_comment_page, callback=self.parse_comment_page)




