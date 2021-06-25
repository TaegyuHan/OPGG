"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailRune

   데이터 입력 code
"""


import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from crawling.opgg_statistics_detail_rune import OpggStatisticsDetailRune




class PreprocessStatisticsDetailRune():




    def __init__(self):

        # 로그 설정
        self.logger = log.make_logger("Preprocess Data")
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))

        # 크롤링 가져오기
        self.crawling = OpggStatisticsDetailRune()




    def prepro_champion_detail_rune(self, champ_num, champ_line):
        """ 크롤링한 데이터를 DB에 넣기 전에
            전처리 합니다.
            craling func : champion_detail_rune

        Args:
            champ_num ([int]): 챔피언 번호
              ex ) : 266

            champ_line ([string]): 챔피언 가는 라인 대문자
              ex ) : "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"

        Returns:
            [json]: 스킬 정보
                ex ) : {
                          "0": {
                            "Style": 8000,
                            "Keystone": 8010,
                            "Substyle": 8400,
                            "PickPercentage": 75.59,
                            "WinRate": 51.57,
                            "Detail": {
                              "0": {
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        result_dict = \
          self.crawling.champion_detail_rune(champ_num, champ_line)

        return result_dict




# if __name__ == "__main__":
#     a = PreprocessStatisticsDetailRune()
#     a.prepro_champion_detail_rune(266, "TOP")
