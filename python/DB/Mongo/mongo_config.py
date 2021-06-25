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
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))

        # 접속 경로
        self.client = "mongodb://localhost:27017/"
        self.database = "opgg"
        self.collection = collection_name


    def connect(self):
        """MongoDB 연결

        Returns:
            [class]: <class 'pymongo.cursor.Cursor'>
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            self.client = pymongo.MongoClient(self.client)
            self.db = self.client[self.database] # Database
            self.cursor = self.db[self.collection] # Collection
            self.logger.info("FUC | {} > success".format(sys._getframe().f_code.co_name))
            

            return self.cursor

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



