# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailSkill 
                
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

from crawling.opgg_statistics_detail_skill \
  import OpggStatisticsDetailSkill # 전처리 class




def insert_statistics_detail_skill(collection):
    """ 
        크롤링한 데이터를 DB에 넣습니다.

        crawling_func :
            champion_detail_skill()
    """

    logger = log.make_logger("MongoDB_DB")
    logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))


    MongoDB_champ_info = MongoDB_DB("championInfo")
    MongoDB = MongoDB_DB(collection)

    cursor_insert = MongoDB.connect()
    cursor_find = MongoDB_champ_info.connect()


    CRAWLING = OpggStatisticsDetailSkill() # 크롤링 연결
    url_list = CRAWLING.champion_line_url() # URL 가져오기


    # 챔피언 URL을 가지고
    # 이름과 라인 추출
    for url in url_list:
        champ_line = url.split("/")[-1].upper()
        champ_name = url.split("/")[-3
        ].capitalize().replace("'", "").replace(".", "").replace(" ", "")

        champ_name_change = {
            "Aurelionsol":"AurelionSol",
            "Drmundo":"DrMundo",
            "Jarvaniv":"JarvanIV",
            "Kogmaw":"KogMaw",
            "Leesin":"LeeSin",
            "Masteryi":"MasterYi",
            "Missfortune":"MissFortune",
            "Reksai":"RekSai",
            "Tahmkench":"TahmKench",
            "Twistedfate":"TwistedFate",
            "Wukong" : "WuKong", # 오공 json 데이터 없음
            "Xinzhao":"XinZhao",
        }
        
        # 챔피언 이름 중간 소문자 대문자로 변경
        for key, val in champ_name_change.items():
            if key == champ_name:
                champ_name = val

        # 챔피언 번호 추출
        for dict in cursor_find.find({"champName":champ_name}):
            champ_number = dict["data"][champ_name]["key"]

        # 예외 처리 오공 json 데이터 없음
        # 따라서 직접 넣어줌
        if champ_name == "WuKong":
            champ_number = 62

        # data 가져오기
        data = CRAWLING.champion_detail_skill(url, champ_number, champ_line)
        
        try:
            data = json.dumps(data)
            data = json.loads(data)
            cursor_insert.insert_one(data)
        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



if __name__ == '__main__':

    collection = "championDetailSkill"
    insert_statistics_detail_skill(collection)
