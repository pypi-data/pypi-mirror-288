import unittest
import os
from scraper_hj3415.krx import krx300


class KrxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.TEMP_DIR = os.path.join(os.getcwd(), '_down_krx')
        self.EXCEL_FILE = os.path.join(self.TEMP_DIR, 'PDF_DATA.xls')

    def tearDown(self):
        pass

    def test_download_krx300(self):
        krx300.download_krx300(self.TEMP_DIR, headless=False)

    def test_get(self):
        # 아래 테스트는 파일저장 문제로 제대로 작동안됨. 파일저장 에러시 대처를 위한 테스트로 사용할 것
        krx300.get(headless=False)

