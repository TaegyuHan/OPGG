# -*- coding: utf-8 -*-

import sys
import os
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그


def insert_champion_info(collection):

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | insert_champion_info > run")

    try:
        # json file 경로
        json_directory_path = Path("C:\github\OPGG\json\ko_KR\champion")
        json_file_path_iter = json_directory_path.iterdir()
        
        # 저장 리스트
        insert_list = []

        # json file read
        for fp in json_file_path_iter:

            # JSON file
            f = open (fp, "r", encoding='UTF8')

            # Reading from file
            data = json.loads(f.read())
            # Iterating through the json

            insert_list.append(data)
            # print(data)

            # Closing file
            f.close()

        # DB 연결
        MongoDB = MongoDB_DB(collection)

        # 리스트 DB insert
        cursor = MongoDB.connect()
        cursor.insert_many(insert_list)
    
    except:
        logger.error("FUC | insert_champion_info > error")


if __name__ == '__main__':

    collection = "championInfo"
    insert_champion_info(collection)
