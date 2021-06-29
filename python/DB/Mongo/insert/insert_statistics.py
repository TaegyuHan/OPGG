# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championInfochampionStatisticsInfo,
                championStatisticsBanInfo
                
   데이터 입력 code
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from DB.PreprocessData.preprocess_statistics import PreprocessStatistics




def insert_statistics(collection):
    """ 크롤링한 데이터를 전처리 후
        DB에 넣습니다.

        preprocess_func :
            prepro_champion_statistics_info()

    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

    try:
        PS = PreprocessStatistics()
        list_data = PS.prepro_champion_statistics_info()

        # Iterating through the json
        print(list_data)

        # # DB 연결
        MongoDB = MongoDB_DB(collection)

        # # 리스트 DB insert
        cursor = MongoDB.connect()
        cursor.insert_many(list_data)
    
    except:
        logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




def insert_statistics_ban(collection):
    """ 크롤링한 데이터를 전처리 후
        DB에 넣습니다.

        preprocess_func :
            prepro_champion_statistics_ban_info()
            
    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

    try:
        PS = PreprocessStatistics()
        list_data = PS.prepro_champion_statistics_ban_info()

        # Iterating through the json
        print(list_data)

        # # DB 연결
        MongoDB = MongoDB_DB(collection)

        # # 리스트 DB insert
        cursor = MongoDB.connect()
        cursor.insert_many(list_data)
    
    except:
        logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




# if __name__ == '__main__':

#     collection = "championStatisticsInfo"
#     insert_statistics(collection)

#     collection = "championStatisticsBanInfo"
#     insert_statistics_ban(collection)
