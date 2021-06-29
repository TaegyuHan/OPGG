# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailSynthesize
                
   데이터 입력 code
"""

import sys
import os
import json
from time import sleep

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB # DB class

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그

from crawling.opgg_statistics_detail_synthesize \
  import OpggStatisticsDetailSynthesize # 전처리 class


def insert_statistics_detail_synthesize(collection = "championDetailSynthesize"):
    """크롤링한 데이터를 DB에 넣습니다.

        crawling_func :
            champion_detail_synthesize()    

    Args:
        collection (str, optional): collection 이름
        [description]. Defaults to "championDetailSynthesize".
    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

    try:
        CRAWLING = OpggStatisticsDetailSynthesize() # 크롤링 연결
        url_list = CRAWLING.champion_line_url() # URL 가져오기

        # DB 연결
        MongoDB = MongoDB_DB(collection)

        # 리스트 DB insert
        cursor = MongoDB.connect()

        for url in url_list:

            data = CRAWLING.champion_detail_synthesize(url)
            print(data)
            sleep(1)
            try:
                data = json.dumps(data)
                data = json.loads(data)
                cursor.insert_one(data)

            except:
              logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))
              continue

    except:
        logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))


# if __name__ == '__main__':

#     collection = "championDetailSynthesize"
#     insert_statistics_detail_synthesize(collection)
