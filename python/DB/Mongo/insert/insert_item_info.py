# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : itemInfo

   데이터 입력 code
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그


def insert_item_info(collection):

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | insert_item_info > run")

    try:

        json_file_path = "C:\github\OPGG\json\ko_KR\item.json"

        # JSON file
        f = open (json_file_path, "r", encoding='UTF8')

        # Reading from file
        json_data = json.loads(f.read())
        # Iterating through the json

        print(json_data)

        # Closing file
        f.close()

        # DB 연결
        MongoDB = MongoDB_DB(collection)

        # 리스트 DB insert
        cursor = MongoDB.connect()
        cursor.insert_one(json_data)
    
    except:
        logger.error("FUC | insert_item_info > error")


if __name__ == '__main__':

    collection = "itemInfo"
    insert_item_info(collection)
