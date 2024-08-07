from scraper_hj3415.krx import krx300
from utils_hj3415 import utils
import argparse
import os
import json

# 파일에 저장할 데이터의 기본 파일 경로
FILE_PATH = 'settings.json'
mongo_addr_title = 'mongo_addr'


def save_addr(address: str):
    """주소를 파일에 저장합니다."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            settings = json.load(file)
    else:
        settings = {
        }

    settings[mongo_addr_title] = address

    with open(FILE_PATH, 'w') as file:
        json.dump(settings, file, indent=4)

    print(f"주소가 저장 되었습니다: {address}")


def load_addr() -> str:
    """파일에서 주소를 불러옵니다."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            settings = json.load(file)
            return settings[mongo_addr_title]
    else:
        # 기본값
        return "mongodb://hj3415:piyrw421@192.168.100.175:27017/"


def db():
    parser = argparse.ArgumentParser(description="데이터베이스 주소를 저장하고 불러오는 프로그램")
    subparsers = parser.add_subparsers(dest='command', help='명령을 선택하세요.')

    # 저장 서브커맨드
    parser_save = subparsers.add_parser('save', help='데이터베이스 주소를 저장합니다.')
    parser_save.add_argument('address', type=str, help='저장할 주소를 입력하세요.')

    # 불러오기 서브커맨드
    parser_load = subparsers.add_parser('print', help='저장된 데이터베이스 주소를 불러옵니다.')

    # 인자 파싱
    args = parser.parse_args()

    # 명령에 따른 동작 수행
    if args.command == 'save':
        save_addr(args.address)
    elif args.command == 'print':
        address = load_addr()
        if address:
            print(f"데이터베이스 주소: {address}")


def nfs():
    from scraper_hj3415.nfscraper import run_nfs
    spiders = {
        'c101': run_nfs.c101,
        'c106': run_nfs.c106,
        'c103y': run_nfs.c103y,
        'c103q': run_nfs.c103q,
        'c104y': run_nfs.c104y,
        'c104q': run_nfs.c104q,
        'c108': run_nfs.c108,
        'all_spider': run_nfs.all_spider
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders.keys()}")
    parser.add_argument('targets', nargs='+', type=str, help="원하는 종류의 코드를 나열하세요.")

    args = parser.parse_args()

    if args.spider in spiders.keys():
        if len(args.targets) == 1 and args.targets[0] == 'all':
            #x = input("It will take a long time. Are you sure? (y/N)")
            #if x == 'y' or x == 'Y':
            # krx300 에서 전체코드리스트를 가져와서 섞어준다.
            import random
            all_codes = krx300.get()
            random.shuffle(all_codes)
            spiders[args.spider](*all_codes)
        else:
            # args.targets의 코드 유효성을 검사한다.
            is_valid = True
            for code in args.targets:
                # 하나라도 코드 형식에 이상 있으면 에러
                is_valid = utils.is_6digit(code)
            if is_valid:
                spiders[args.spider](*args.targets)
            else:
                print(f"{args.targets} 종목 코드의 형식은 6자리 숫자입니다.")
    else:
        print(f"The spider should be in {list(spiders.keys())}")

"""
def miscraper():
    spiders = ['mihistory', 'mi']

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders}")

    parser.add_argument('-d', '--db_path', help="Set mongo database path")
    args = parser.parse_args()

    if args.spider in spiders:
        if args.spider == 'mihistory':
            years = 2
            print(f"We will collect MI data for past {years} years.")
            mirun.mi_history(years, args.db_path) if args.db_path else mirun.mi_history(years)
        elif args.spider == 'mi':
            mirun.mi_all(args.db_path) if args.db_path else mirun.mi_all()
    else:
        print(f"The spider option should be in {spiders}")
"""
