import json

import scrapy


class MoocChinaSpider(scrapy.Spider):
    name = "mooc-china-user"

    # memberId
    user_info_url_pattern = 'https://www.icourse163.org/web/j/memberBean.getMocMemberPersonalDtoById.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    learn_statistic_url_pattern = 'https://www.icourse163.org/web/j/learnerCourseRpcBean.getPersonalLearningStatisticDto.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    # uid: 4947184
    # pageIndex: 1
    # pageSize: 32
    learn_list_url_pattern = 'https://www.icourse163.org/web/j/learnerCourseRpcBean.getOtherLearnedCoursePagination.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    current_user_id = None
    user_info_data_object = None
    user_learn_list = []

    def start_requests(self):

        user_ids = set()

        with open('aaaaaa.json', 'r') as reader:
            pre_data = json.load(reader)
        reader.close()

        for comment in pre_data:
            user_ids.add(comment['commentorId'])

        for user_id in user_ids:

            self.current_user_id = user_id

            user_info_data = {
                'menberId': str(user_id),
            }

            user_info_request = scrapy.FormRequest(url=self.user_info_url_pattern, headers=self.headers, formdata=user_info_data, callback=self.parse_user_info)
            yield user_info_request

            print('after 1111111111111')

            learn_list_data = {
                'uid': str(user_id),
                'pageIndex': '1',
                'pageSize': '32',
            }
            learn_list_request = scrapy.FormRequest(url=self.learn_list_url_pattern, headers=self.headers, formdata=learn_list_data, callback=self.parse_learn_list)
            yield learn_list_request

            print('after 2222222222222')

            yield {
                'userInfo': self.user_info_data_object,
                'userLearn': self.user_learn_list,
            }

            print('after 3333333333333')

            self.user_info_data_object = None
            self.user_learn_list = []

    def parse(self, response):
        resp = json.loads(response.body)

        result = resp['result']

        for course in result['result']:
            # fetch commit here
            school_short_cut = course['schoolPanel']['shortName']
            id_num = course['id']
            course_id = school_short_cut + str(id_num)
            course_url = 'https://www.icourse163.org/course/course-' + course_id

            yield course

    def parse_user_info(self, response):
        resp = json.loads(response.body)
        self.user_info_data_object = resp['result']

    def parse_learn_list(self, response):
        resp = json.loads(response.body)
        print('qqqqqqqqqqqqll', resp)
        result = resp['result']
        print('rrrrrrrrrrrrrr', result)
        self.user_learn_list.append(result['list'])

        if result['query']['totlePageCount'] > 1 and result['query']['totlePageCount'] != result['query']['indexPage']:
            learn_list_data = {
                'uid': str(self.current_user_id),
                'pageIndex': str(result['query']['pageIndex'] + 1),
                'pageSize': '32',
            }
            learn_list_request = scrapy.FormRequest(url=self.learn_list_url_pattern, headers=self.headers, formdata=learn_list_data, callback=self.parse_learn_list)
            yield learn_list_request



