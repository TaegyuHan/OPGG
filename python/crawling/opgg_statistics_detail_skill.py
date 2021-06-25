"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/{}/statistics/{}/skill
  OpggStatisticsDetailSkill 클래스 정의 코드

"""


import re
import os
import sys
from time import sleep

sys.path.append(os.path.dirname(__file__))
from opgg_statistics_detail import OpggStatisticsDetail


class OpggStatisticsDetailSkill(OpggStatisticsDetail):




    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))




    def champion_detail_skill(self, champ_num, champ_line):
        """OPGG 챔피언 세부 스킬 page 정보

        Args:
            champ_num ([int]): 챔피언 번호
              ex ) : 266

            champ_line ([string]): 챔피언 가는 라인 대문자
              ex ) : "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"

        Returns:
            [json]: 스킬 정보
                ex ) : {'021': {'PickPercentage': '62.51',
                                'WinRate': '99.82',
                                'SkillBuild': {0: {'Sequence': ['Q', 'E', ...
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            # 결과 딕셔너리
            result_dict = {}

            html = \
              self.read_html("https://www.op.gg/champion/aatrox/statistics/top/skill")
            
            # 이미지 정규식
            pattern = "([-\w]+\.(?:jpg|gif|png|jpeg))"
            
            # skill header 추출
            ul = \
              html.find("ul", class_="champion-stats__filter champion-stats__filter tabHeaders")

            ul_list = ul.find_all("ul", class_="champion-stats__list")
            div = ul.find_all("div", class_="champion-stats__filter__item__values")

            for i in range(len(ul_list)):
                il = []
                li = \
                  ul_list[i].find_all("li", class_="champion-stats__list__item tip")

                # 스킬 해더 승률
                winrate = \
                  float(
                    div[i].find("div", class_="champion-stats__filter_item_value--winrate"
                    ).find("b").get_text().replace("%", "")
                  )

                # 스킬 해더 픽률
                pickrate = \
                  float(
                    div[i].find("div", class_="champion-stats__filter_item_value--pickrate"
                    ).find("b").get_text().replace("%", "")
                  )

                # 스킬 해더 key 만들기
                for j in range(len(li)):
                    img_src = li[j].find("img")["src"]
                    skill_image = re.search(pattern, img_src).group()
                    num = skill_image.find(".") - 1 # 스킬 추출 번호
                    il.append(skill_image[num])
                
                skill_type = ''.join(il)
                skill_type = skill_type.replace("Q", "0").replace("W", "1").replace("E", "2")

                # 입력
                result_dict[skill_type] = {}
                result_dict[skill_type]["PickPercentage"] = pickrate
                result_dict[skill_type]["WinRate"] = winrate

            # 키, 번호, 라인 ajax 검색
            for skill_type in result_dict.keys():
                url_format_num = ",".join(skill_type)

                self.SKILL_AJAX_URL = "https://www.op.gg/champion/ajax/statistics/skillList/championId={}&position={}&skillPriority={}&"
                
                URL = self.SKILL_AJAX_URL.format(champ_num, # 챔피언 번호
                                                 champ_line, # 라인 "MID"
                                                 url_format_num )

                # print(URL)
                html = self.read_html(URL)
                sleep(1)

                # 스킬 순서
                tbody_skill = html.find_all("table", class_="champion-skill-build__table")

                # 스킬 픽률
                tbody_pickrate = html.find_all("td", class_="champion-stats__table__cell--pickrate")

                # 스킬 승률
                tbody_winrate = html.find_all("td", class_="champion-stats__table__cell--winrate")
                
                result_dict[skill_type]["SkillBuild"] = {}

                for i in range(len(tbody_skill)):
                    skill_list = tbody_skill[i].find_all("td")

                    result_dict[skill_type]["SkillBuild"][i] = {}
                    result_dict[skill_type]["SkillBuild"][i]["Sequence"] = []

                    # 스킬 픽률
                    pickrate = \
                      tbody_pickrate[i].get_text().replace(" ", "").strip().split("%")

                    result_dict[skill_type]["SkillBuild"][i]["PickPercentage"] = \
                      float(pickrate[0])

                    result_dict[skill_type]["SkillBuild"][i]["PickCount"] = \
                      int(pickrate[1].replace(",", ""))

                    # 스킬 승률
                    result_dict[skill_type]["SkillBuild"][i]["WinRate"] = \
                      float(
                        tbody_winrate[i].get_text().replace("%","")
                      )

                    # 스킬 순서
                    for j in range(len(skill_list)):
                        skill = skill_list[j].get_text().strip()
                        result_dict[skill_type]["SkillBuild"][i]["Sequence"].append(skill)

            return result_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



