# -*- coding: utf-8 -*-

""" 
    MongoDB 연결 core code

"""

import pymongo
import sys


sys.path.append("..\\..\\")
from log import log # 로그



class MongoDB_DB():




    def __init__(self, collection_name):
        """MongoDB 연결

        Args:
            collection_name ([string]): collection 이름 입력
                ex ) : "customers"

        Returns:
            [class]: <class 'pymongo.cursor.Cursor'>
        """

        # 로그 생성
        self.logger = log.make_logger("MongoDB_DB")
        self.logger.info("CLASS | MongoDB_DB > run")

        # 접속 경로
        client = "mongodb://localhost:27017/"
        database = "opgg"
        collection = collection_name

        try:
            self.client = pymongo.MongoClient(client)
            self.db = self.client[database] # Database
            self.cursor = self.db[collection] # Collection
            self.logger.info("CLASS | MySQL_DB > success")

        except:
            self.logger.error("CLASS | DB connect | > error")


if __name__ == '__main__':
    a = MongoDB_DB(
        collection_name = "championInfo"
    )
    
