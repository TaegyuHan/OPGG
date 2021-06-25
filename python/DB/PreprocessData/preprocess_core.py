
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
