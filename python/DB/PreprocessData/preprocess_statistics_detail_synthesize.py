"""
   DB : MongoDB
   Database : opgg
   Collection : championDetailSynthesize

   데이터 입력 code
"""


import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from crawling.opgg_statistics_detail_synthesize import OpggStatisticsDetailSynthesize




class PreprocessStatisticsDetailSynthesize():




    def __init__(self):


        # 로그 설정
        self.logger = log.make_logger("Preprocess Data")
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))

        # 크롤링 가져오기
        self.crawling = OpggStatisticsDetailSynthesize()

    
    def prepro_champion_detail_synthesize(self):
        """ 크롤링한 데이터를 DB에 넣기 전에
            전처리 합니다.
            craling func : champion_detail_synthesize

        Returns:
            [dict]: 전처리 결과
                ex) : {
                        "CounterChampion": {
                            "Nocturne": 40.46,
                            "Zac": 41.6,
                            "Heimerdinger": 42.11
                        },
                        "EasyChampion": {
                            "Tahm Kench": 60.78,
                            "Maokai": 57.14,
                        "Lee Sin": 57.07

                        ...
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:

            result_dict = self.crawling.champion_detail_synthesize()

            return result_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



# if __name__ == "__main__":
#     a = PreprocessStatisticsDetailSynthesize()
#     a.prepro_champion_detail_synthesize()    