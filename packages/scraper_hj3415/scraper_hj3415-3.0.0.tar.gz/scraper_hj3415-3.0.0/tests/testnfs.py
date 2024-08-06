import unittest
from db_hj3415 import mongo
from scraper_hj3415.nfscraper import run_nfs


class NfsTest(unittest.TestCase):
    def setUp(self) -> None:
        # self.addr = "mongodb://192.168.0.175:27017"
        self.addr = run_nfs.addr
        self.client = mongo.connect_mongo(self.addr)
        mongo.Base.initialize_client(self.client)
        self.test_codes = ['005930', '005490', '006840']
        self.is_drop_db = True

    def tearDown(self):
        if self.is_drop_db:
            print(f"drop test codes {self.test_codes} on tearDown")
            for code in self.test_codes:
                mongo.Corps.drop_db(code)
        else:
            print('pass delete db on tearDown')
        self.client.close()

    def test_make_c101_dummy(self):
        self.is_drop_db = False
        run_nfs.c101(*self.test_codes)

    def test_make_c106_dummy(self):
        self.is_drop_db = False
        #self.test_codes = ['005930', ]
        run_nfs.c106(*self.test_codes)

    def test_make_c103y_dummy(self):
        self.is_drop_db = False
        # self.test_codes = ['005930',]
        run_nfs.c103y(*self.test_codes)

    def test_make_c103q_dummy(self):
        self.is_drop_db = False
        # self.test_codes = ['005930',]
        run_nfs.c103q(*self.test_codes)

    def test_make_c104y_dummy(self):
        self.is_drop_db = False
        # self.test_codes = ['005930',]
        run_nfs.c104y(*self.test_codes)

    def test_make_c104q_dummy(self):
        self.is_drop_db = False
        self.test_codes = ['005930',]
        run_nfs.c104q(*self.test_codes)

    def test_make_c108_dummy(self):
        self.is_drop_db = True
        self.test_codes = ['005930',]
        run_nfs.c108(*self.test_codes)

    def test_all(self):
        self.is_drop_db = False
        #self.test_codes = ['005930',]
        run_nfs.all(*self.test_codes)

    # 몽고에서 회사 디비를 청소하기 위한 유틸테스터
    def test_drop_all_codes(self):
        self.is_drop_db = False
        print(mongo.Corps.list_all_codes())
        mongo.Corps.drop_all_codes()
        print(mongo.Base.list_db_names())

    def test_krx300_all(self):
        from scraper_hj3415.krx import krx300
        self.is_drop_db = False
        l = krx300.get()
        run_nfs.all(*l)

    def test_krx300_c101(self):
        from scraper_hj3415.krx import krx300
        self.is_drop_db = False
        l = krx300.get()
        run_nfs.c101(*l)






