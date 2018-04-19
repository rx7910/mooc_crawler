import json
import scrapy


class MoocChinaSpider(scrapy.Spider):
    name = "mooc-china-user"

    # memberId
    user_info_url_pattern = 'https://www.icourse163.org/web/j/memberBean.getMocMemberPersonalDtoById.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    # learn_statistic_url_pattern = 'https://www.icourse163.org/web/j/learnerCourseRpcBean.getPersonalLearningStatisticDto.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    # uid: 4947184
    # pageIndex: 1
    # pageSize: 32
    learn_list_url_pattern = 'https://www.icourse163.org/web/j/learnerCourseRpcBean.getOtherLearnedCoursePagination.rpc?csrfKey=4e1578f4af174b65b9291cdd6acd1d92'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    current_user_id = None
    user_info_data_object_mapper = {}
    user_learn_list_mapper = {}

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
                'memberId': str(user_id),
            }

            meta_data = {
                'userId': str(user_id),
            }

            user_info_request = scrapy.FormRequest(
                meta=meta_data,
                url=self.user_info_url_pattern,
                headers=self.headers,
                formdata=user_info_data,
                callback=self.parse_user_info,
            )
            yield user_info_request

    def parse_user_info(self, response):
        resp = json.loads(response.body)
        user_id = response.meta['userId']

        if str(resp['result']['memberId']) != user_id:
            raise Exception('user_id doesn\'t match with response')
        self.user_info_data_object_mapper[str(resp['result']['memberId'])] = resp['result']

        learn_list_data = {
            'uid': user_id or str(resp['result']['memberId']),
            'pageIndex': '1',
            'pageSize': '32',
        }

        meta_data = {
            'userId': user_id,
        }
        learn_list_request = scrapy.FormRequest(
            meta=meta_data,
            url=self.learn_list_url_pattern,
            headers=self.headers,
            formdata=learn_list_data,
            callback=self.parse_learn_list,
        )
        yield learn_list_request

    def parse_learn_list(self, response):
        resp = json.loads(response.body)
        result = resp['result']
        user_id = response.meta['userId']

        if user_id not in self.user_learn_list_mapper:
            self.user_learn_list_mapper[user_id] = []

        # insert data
        if result['list'] is not None and len(result['list']) > 0:

            if str(result['list'][0]['uid']) != user_id:
                raise Exception('user_id does not match with response')

            self.user_learn_list_mapper[user_id].append(result['list'])

        # raise another request or yield data
        if result['query']['totlePageCount'] > 1 and result['query']['totlePageCount'] != result['query']['pageIndex']:
            learn_list_data = {
                'uid': user_id or str(self.current_user_id),
                'pageIndex': str(result['query']['pageIndex'] + 1),
                'pageSize': '32',
            }
            meta_data = {
                'userId': user_id,
            }
            learn_list_request = scrapy.FormRequest(
                url=self.learn_list_url_pattern,
                headers=self.headers,
                formdata=learn_list_data,
                callback=self.parse_learn_list,
                meta=meta_data,
            )
            yield learn_list_request
        else:
            yield {
                'userInfo': self.user_info_data_object_mapper[user_id],
                'userLearn': self.user_learn_list_mapper[user_id],
            }

'''
data format as follow:

[
    {
        userInfo: {
            department: null,
            description: "",
            followCount: 0,
            followStatus: false,
            followedCount: 0,
            highestDegree: 5,
            isTeacher: false,
            jobName: null,
            largeFaceUrl: "",
            lectorTitle: null,
            logoForCertUrl: null,
            memberId: 1136787461,
            memberType: 1,
            nickName: "杨素素201709",
            realName: null,
            richDescription: null,
            schoolId: null,
            schoolName: null,
            schoolShortName: null,
            supportCommonMooc: null,
            supportMooc: null,
            supportPostgradexam: null,
            supportSpoc: null,
        },
        userLearn: [
            {
                courseCoverUrl : "http://edu-image.nosdn.127.net/30CD34C01C7BBA7AABC0E04C8A39AFD3.jpg?imageView&thumbnail=510y288&quality=100",
                courseId : 1002599007,
                courseName : "工尺谱概论",
                courseProductType : 1,
                enrollCount : 1608,
                mode : 0,
                schoolId : 1001439001,
                schoolName : "中央音乐学院",
                schoolShortName : "CCOM",
                supportCommonMooc : null,
                termId : 1002781027,
                uid : 1136787461,
                whatCertGot : null,
            },
            {
                ...   
            },
            {
                ...   
            },
            {
                ...   
            },
        ],
    },
    {
        ...
    },
    {
        ...
    },
    {
        ...
    },
]

'''




