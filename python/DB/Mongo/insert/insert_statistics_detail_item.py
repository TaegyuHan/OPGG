# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailItem  
                
   데이터 입력 code
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB # DB class

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그

from crawling.opgg_statistics_detail_item \
  import OpggStatisticsDetailItem # 전처리 class


def insert_statistics_detail_item(collection="championDetailItem"):
    """ 
        크롤링한 데이터를 DB에 넣습니다.

        crawling_func :
            champion_detail_item()

    Args:
        collection (str, optional): collection 이름
        [description]. Defaults to "championDetailItem".
    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

    # 챔피언 skill 정보 insert DB 연결
    MongoDB = MongoDB_DB(collection)
    cursor_insert = MongoDB.connect()

    CRAWLING = OpggStatisticsDetailItem() # 크롤링 연결
    url_list = CRAWLING.champion_line_url() # URL 가져오기

    for url in url_list:

      data = CRAWLING.champion_detail_item(url)

      try:
         data = json.dumps(data)
         data = json.loads(data)
         cursor_insert.insert_one(data)

      except:
         self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



if __name__ == '__main__':

    collection = "championDetailItem"
    insert_statistics_detail_item(collection)
