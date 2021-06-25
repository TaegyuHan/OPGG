
from posixpath import expanduser
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그




class PreprocessCore():




    def __init__(self):

        # 로그 설정
        self.logger = log.make_logger("Preprocess Data")
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))




    def chage_PPW(self, tmp_dict, input_key):
        """json 데이터에서

            "SkillBuild": {
              "Sequence": [
                "Q",
                "E",
                "W",
                "Q",
                "Q",
                "R",
                "Q",
                "E",
                "Q",
                "E",
                "R",
                "E",
                "E",
                "W",
                "W"
              ],
              "PickPercentage": "91.34",
              "PickCount": "1,360",
              "WinRate": "62.57"
            },

          번호형으로 됀 dict 안에 
              "PickPercentage": "91.34", > 91.34
              "PickCount": "1,360", > 1,360
              "WinRate": "62.57" > 62.57
          수정 string > int, float

        Args:
            tmp_dict ([type]): [description]
            input_key ([type]): [description]
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            tmp_dict[input_key]["PickPercentage"] = \
                float(tmp_dict[input_key]["PickPercentage"])

            tmp_dict[input_key]["PickCount"] = \
                int(tmp_dict[input_key]["PickCount"].replace(",", ""))

            tmp_dict[input_key]["WinRate"] = \
                float(tmp_dict[input_key]["WinRate"])

            return tmp_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




    def chage_num_PPW(self, tmp_dict, input_key):
        """json 데이터에서

            "Spell": {
              "0": {
                "SpellImage": [
                  "SummonerFlash.png",
                  "SummonerTeleport.png"
                ],
                "PickPercentage": "97.53",
                "PickCount": "3,439",
                "WinRate": "49.46"
              },
              "1": {
                "SpellImage": [
                  "SummonerFlash.png",
                  "SummonerDot.png"
                ],
                "PickPercentage": "2.01",
                "PickCount": "71",
                "WinRate": "66.2"
              }
            }

          번호형으로 됀 dict 안에 
                "PickPercentage": "2.01", > 2.01
                "PickCount": "71", > 71
                "WinRate": "66.2" > 66.2
          수정 string > int, float

        Args:
            tmp_dict ([dict]]) : json 딕셔너리
            input_key ([string]): json 딕셔너리 키값

        Returns:
            [dict]: 변경후의 json 값
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            for k in tmp_dict[input_key].keys():
      
                tmp_dict[input_key][k]["PickPercentage"] = \
                    float(tmp_dict[input_key][k]["PickPercentage"])
                
                # 에러 때문에 tmp 생성
                tmp_dict[input_key][k]["PickCount"] = \
                    int(tmp_dict[input_key][k]["PickCount"].replace(",", ""))
                    

                tmp_dict[input_key][k]["WinRate"] = \
                    float(tmp_dict[input_key][k]["WinRate"])

            return tmp_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




    def chage_item(self, tmp_dict, input_key):
        """dict의 item 들의 .png 형태를
           int 형으로 변환후 return 합니다.

              {
                "Images": [
                  "1054.png", > 1054
                  "2003.png"  > 2003
                ],
                "PickPercentage": "64.53",
                "PickCount": "2,230",
                "WinRate": "48.79%"
              }

        Args:
            tmp_dict ([dict]): dict 형태 정보
                               dict안에 list 형의 image 정보만
                               변환이 가능합니다.

            input_key ([string]): 변환 list의 키를 입력합니다.
                ex ) : "Images"

        Returns:
            [dict]: 변환 후 결과 dict를 반환 합니다.
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
          for i in range(len(tmp_dict[input_key])):

              tmp_dict[input_key][i] = \
                  int(tmp_dict[input_key][i].split(".")[0])

          return tmp_dict
          
        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))