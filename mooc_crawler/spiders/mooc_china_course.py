import json

import scrapy

class MoocChinaSpider(scrapy.Spider):
    name = "mooc-china-course"
    url_pattern = 'https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=ce9ad61e1cd140b98685c9a2bf1547ae'
    all_symbols = 73

    commit_url_pattern = 'https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=ce9ad61e1cd140b98685c9a2bf1547ae'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    course_name = None
    course_id = None

    def start_requests(self):
        url = 'https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=ce9ad61e1cd140b98685c9a2bf1547ae'
        data = {
            'categoryId': '-1',
            'type': '30',
            'orderBy': '0',
            'pageIndex': '2',
            'pageSize': '20',
        }
        symbols = self.all_symbols
        for symbol in range(symbols):
            data = {
                'categoryId': '-1',
                'type': '30',
                'orderBy': '0',
                'pageIndex': str(symbol),
                'pageSize': '20',
            }
            form_request = scrapy.FormRequest(url=url, headers=self.headers, formdata=data)
            yield form_request

        # yield FormRequest(url, headers=self.headers, formdata=data)

    def parse(self, response):
        resp = json.loads(response.body)

        result = resp['result']

        for course in result['result']:
            # fetch commit here
            school_short_cut = course['schoolPanel']['shortName']
            id_num = course['id']
            course_id = school_short_cut + str(id_num)
            course_url = 'https://www.icourse163.org/course/course-' + course_id
            self.course_name = course['name']
            self.course_id = course['id']

            yield course
