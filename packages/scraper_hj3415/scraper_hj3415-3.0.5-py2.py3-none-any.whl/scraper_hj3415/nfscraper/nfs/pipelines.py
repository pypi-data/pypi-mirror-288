# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from db_hj3415 import mongo
import pprint
from pymongo.errors import BulkWriteError
from utils_hj3415 import noti


class ValidationPipeline:
    def process_item(self, item, spider):
        print(f"\tIn ValidationPipeline.. code : {item['code']} / page : {item['page']}")
        if spider.name == 'c101':
            print(f"\t\tRaw data - EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
            if mongo.Corps.is_there(code=item['code'], page='c104q'):
                c104q = mongo.C104(item['code'], 'c104q')
                # print('\t\tEPS', c104q.find('EPS', remove_yoy=True)[1])
                # print('\t\tBPS', c104q.find('BPS', remove_yoy=True)[1])
                d, cal_eps = c104q.sum_recent_4q('EPS')  # 최근 4분기 eps값을 더한다.
                d, cal_bps = c104q.latest_value('BPS')  # 마지막 분기 bps값을 찾는다.

                # per, pbr을 구하는 람다함수
                cal_ratio = (lambda eps_bps, pprice:
                             None if eps_bps is None or eps_bps == 0 else round(int(pprice) / int(eps_bps), 2))
                cal_per = cal_ratio(cal_eps, item['주가'])
                cal_pbr = cal_ratio(cal_bps, item['주가'])
                print(f"\t\tCalc data - EPS:{cal_eps} BPS:{cal_bps} PER:{cal_per} PBR:{cal_pbr}")
                item['EPS'], item['BPS'], item['PER'], item['PBR'] = cal_eps, cal_bps, cal_per, cal_pbr
            else:
                print("\t\tc104q 데이터가 없어서 c101 데이터를 사용합니다..")
        elif 'c103' in spider.name:
            pass
        elif 'c104' in spider.name:
            pass
        elif spider.name == 'c106':
            pass
        elif spider.name == 'c108':
            pass
        return item


class MongoPipeline:
    def process_item(self, item, spider):
        print(f"\tIn MongoPipeline.. code : {item['code']} / page : {item['page']}")
        if spider.name == 'c101':
            # print(item)
            mongo.C101.save(item['code'], ItemAdapter(item).asdict())
        elif 'c103' in spider.name:
            # pprint.pprint(item['df'])
            mongo.C103.save(item['code'], item['page'], item['df'])
        elif 'c104' in spider.name:
            # pprint.pprint(item['df'])
            try:
                mongo.C104.save(item['code'], item['page'], item['df'])
            except BulkWriteError as e:
                err_str = f"{item['code']} / {item['page']} 서버 저장에 문제가 있습니다.({str(e)[:60]}..)"
                print(err_str, file=sys.stderr)
                noti.telegram_to('manager', err_str)
        elif spider.name == 'c106':
            # pprint.pprint(item['df'])
            mongo.C106.save(item['code'], item['page'], item['df'])
        elif spider.name == 'c108':
            # pprint.pprint(item['df'].to_dict('records'))
            mongo.C108.save(item['code'], item['df'])
        return item
