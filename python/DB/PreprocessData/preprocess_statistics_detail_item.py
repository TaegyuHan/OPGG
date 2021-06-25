"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailItem

   데이터 입력 code
"""


import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from crawling.opgg_statistics_detail_item import OpggStatisticsDetailItem




class PreprocessStatisticsDetailRune():




    def __init__(self):

        # 로그 설정
        self.logger = log.make_logger("Preprocess Data")
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))

        # 크롤링 가져오기
        self.crawling = OpggStatisticsDetailItem()


    def prepro_champion_detail_item(self):
        """ 크롤링한 데이터를 DB에 넣기 전에
            전처리 합니다.
            craling func : champion_detail_item

        Returns:
            [json]: 아이템 정보
            ex ) : {
                      "CoreBuild": {
                        "0": {
                          "item": [
                            6630,
                            3053,
                            6333
                          ],
                          "PickPercentage": 19.19,
                          "PickCount": 176,
                          "WinRate": 60.23
                        },
                        "1": {
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            result_dict = \
            self.crawling.champion_detail_item()
            
            return result_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



# if __name__ == '__main__':
#     a = PreprocessStatisticsDetailRune()
#     print(a.prepro_champion_detail_item())