import csv
import json
import pandas as pd
import time


def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    f.close()
    return data


def write_csv(data, filename):
    with open(filename, 'w') as outf:
        dw = csv.DictWriter(outf, data[0].keys())
        dw.writeheader()
        for row in data:
            dw.writerow(row)
    outf.close()
write_csv(read_json('./coursescore.json'), './coursescore_all.csv')

data_for_cfr = pd.read_csv('./coursescore_all.csv', usecols=[1, 4, 7, 3])
data_for_cfr['timestamp'] = None

data_for_cfr2 = data_for_cfr.drop([5485, 5825, 7665, 8295])
data_for_cfr2.reset_index(drop=True, inplace=True)


for i in range(len(data_for_cfr2)):
    timeArray = time.strptime(data_for_cfr2.ix[i].createTime, '%Y-%m-%d')
    timestamp = int(time.mktime(timeArray))
    data_for_cfr2.at[i, 'timestamp'] = timestamp

del data_for_cfr2['createTime']

data_for_cfr2.to_csv('./coursescore_for_cfr.csv', index=False, sep='\t')


# new_data = json.dumps(data_for_recsys)
#
# with open('./coursescore_for_recsys.json', 'w', encoding='utf-8') as w:
#     w.write(new_data)
# w.close()
#
# all_data_dist = []
#
# with open('./coursescore.json', 'r') as f:
#     all_data_dist = json.load(f)
# f.close()
#
# new_dist = []
#
#
# class target:
#     def __init__(self, userId, courseId, commentContent, starCount):
#         self.reviewerID = userId
#         self.asin = courseId
#         self.reviewText = commentContent
#         self.overall = starCount
#
#
# for item in all_data_dist:
#     temp = target(userId=item['userId'], courseId=item['courseId'], commentContent=item['commentContent'], starCount=item['starCount'])
#     new_dist.append(temp)
#
# with open('./coursescore_for_recsys.json', 'w') as w:
#     json.dump(new_dist, w)
# w.close()
