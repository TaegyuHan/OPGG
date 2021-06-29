# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailRune
                
   데이터 입력 code
"""

import sys
import os
import json

# 챔피언 이름 라인 함수 호출
from insert_statistics_detail import champ_num_line

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB # DB class

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그

from crawling.opgg_statistics_detail_rune \
  import OpggStatisticsDetailRune # 전처리 class


def insert_statistics_detail_rune(collection="championDetailItem"):
    """ 
        크롤링한 데이터를 DB에 넣습니다.

        crawling_func :
            champion_detail_rune()

    Args:
        collection (str, optional): collection 이름
        [description]. Defaults to "championDetailRune".
    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

    # 챔피언 번호 find DB 연결
    MongoDB_champ_info = MongoDB_DB("championInfo")
    cursor_find = MongoDB_champ_info.connect()

    # 챔피언 skill 정보 insert DB 연결
    MongoDB = MongoDB_DB(collection)
    cursor_insert = MongoDB.connect()

    CRAWLING = OpggStatisticsDetailRune() # 크롤링 연결
    url_list = CRAWLING.champion_line_url() # URL 가져오기

    # 챔피언 URL을 가지고
    # 이름과 라인 추출
    for url in url_list:

      # 챔피언 라인 번호 호출 함수
      champ_number, champ_line = \
          champ_num_line(url, cursor_find)

      # data 가져오기
      data = CRAWLING.champion_detail_rune(url, champ_number, champ_line)

      try:
          data = json.dumps(data)
          data = json.loads(data)
          cursor_insert.insert_one(data)

      except:
          self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




if __name__ == '__main__':

    collection = "championDetailRune"
    insert_statistics_detail_rune(collection)
