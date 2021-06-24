# -*- coding: utf-8 -*-

""" 
    MongoDB 연결 core code

"""

import pymongo
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그



class MongoDB_DB():




    def __init__(self, collection_name):

        # 로그 생성
        self.logger = log.make_logger("MongoDB_DB")
        self.logger.info("CLASS | MongoDB_DB > run")

        # 접속 경로
        self.client = "mongodb://localhost:27017/"
        self.database = "opgg"
        self.collection = collection_name


    def connect(self):
        """MongoDB 연결

        Returns:
            [class]: <class 'pymongo.cursor.Cursor'>
        """

        self.logger.info("FUC | DB connect | > run")

        try:
            self.client = pymongo.MongoClient(self.client)
            self.db = self.client[self.database] # Database
            self.cursor = self.db[self.collection] # Collection
            self.logger.info("FUC | DB connect | > success")

            return self.cursor

        except:
            self.logger.error("FUC | DB connect | > error")



