# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championStatisticsInfo

   데이터 입력 code
"""


import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from crawling.opgg_statistics import OpggStatistics




class PreprocessStatistics():




    def __init__(self):
        
        # 로그 설정
        self.logger = log.make_logger("Preprocess Data")
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))

        # 크롤링 가져오기
        self.crawling = OpggStatistics()




    def prepro_champion_statistics_info(self):
        """ 크롤링한 데이터를 DB에 넣기 전에
            전처리 합니다.
            craling func : champion_statistics_info

        Returns:
            [list]: 전처리 결과
               ex) :  [ {'version': '11.13', 
                         'rankNum': 1, 
                         'changeTierState': 1, 
                         'changeTierValue': 4, 
                         'linePosition': 0, 
                         'championName': 'Fiora', 
                         'goLine': [0, 2], 
                         'winningRate': 51.86, 
                         'pickRate': 9.0, 
                         'tier': 1}, 

                        {'version': '11.13',
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            result_list = []

            # 크롤링 DB 넣기전 전처리
            for tmp_dict in self.crawling.champion_statistics_info():

                # 번호 string > int
                tmp_dict["rankNum"] = int(tmp_dict["rankNum"])

                # changeTierState 챔피언 티어 상태
                # line string > int
                compare = tmp_dict["changeTierState"]

                if compare == "stay":
                    tmp_dict["changeTierState"] = 0
                elif compare == "up":
                    tmp_dict["changeTierState"] = 1
                elif compare == "down":
                    tmp_dict["changeTierState"] = -1
                    
                # 챔피언 상승 값
                tmp_dict["changeTierValue"] = int(tmp_dict["changeTierValue"])

                # 챔피언 포지션
                # line string > int
                compare = tmp_dict["linePosition"]
                if compare == "TOP":
                    tmp_dict["linePosition"] = 0
                elif compare == "JUNGLE":
                    tmp_dict["linePosition"] = 1
                elif compare == "MID":
                    tmp_dict["linePosition"] = 2
                elif compare == "ADC":
                    tmp_dict["linePosition"] = 3
                elif compare == "SUPPORT":
                    tmp_dict["linePosition"] = 4

                # 챔피언 이름
                tmp_dict["championName"]

                # 챔피언 가는 라인
                li = []
                line_list = tmp_dict["goLine"].split(",")
                for line in line_list:
                    line = line.strip()
                    if line == "Top":
                        li.append(0)
                    elif line == "Jungle":
                        li.append(1)
                    elif line == "Middle":
                        li.append(2)
                    elif line == "Bottom":
                        li.append(3)
                    elif line == "Support":
                        li.append(4)

                tmp_dict["goLine"] = li

                # 승률 string > float
                tmp_dict["winningRate"] = float(tmp_dict["winningRate"])
                
                # 픽률 string > float
                tmp_dict["pickRate"] = float(tmp_dict["pickRate"])

                # 티어 strting > int
                tmp_dict["tier"] = int(tmp_dict["tier"])

                result_list.append(tmp_dict)

            return result_list

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




    def prepro_champion_statistics_ban_info(self):
        """ 크롤링한 데이터를 DB에 넣기 전에
            전처리 합니다.
            craling func : champion_statistics_ban_info

        Returns:
            [list]: 전처리 결과
                ex) : [ {'rankNum': 1, 
                         'lineFilter': -1, 
                         'championName': 'Samira', 
                         'banRate': 61.32}, 

                        {'rankNum': 2, 
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            result_list = []

            for tmp_dict in self.crawling.champion_statistics_ban_info():

                # 챔피언 랭크 번호
                tmp_dict["rankNum"] = int(tmp_dict["rankNum"])

                # 챔피언 포지션
                compare = tmp_dict["lineFilter"]
                if compare == "ALL":
                    tmp_dict["lineFilter"] = -1
                elif compare == "TOP":
                    tmp_dict["lineFilter"] = 0
                elif compare == "JUNGLE":
                    tmp_dict["lineFilter"] = 1
                elif compare == "MID":
                    tmp_dict["lineFilter"] = 2
                elif compare == "ADC":
                    tmp_dict["lineFilter"] = 3
                elif compare == "SUPPORT":
                    tmp_dict["lineFilter"] = 4

                # 챔피언 이름
                tmp_dict["championName"]

                #  밴률
                tmp_dict["banRate"] = float(tmp_dict["banRate"])

                result_list.append(tmp_dict)

            return result_list


        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




if __name__ == '__main__':
    a = PreprocessStatistics()
    # print(a.prepro_champion_statistics_info())
    print(a.prepro_champion_statistics_ban_info())



