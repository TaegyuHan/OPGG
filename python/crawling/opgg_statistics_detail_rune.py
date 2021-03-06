"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/{}/statistics/{}/rune
  OpggStatisticsDetailRune 클래스 정의 코드

"""


import re
import sys
import os

from time import sleep

sys.path.append(os.path.dirname(__file__))
from opgg_statistics_detail import OpggStatisticsDetail


class OpggStatisticsDetailRune(OpggStatisticsDetail):




    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))




    def champion_detail_rune(self, url, champ_num, champ_line):
        """OPGG 챔피언 세부 룬 page 정보

        Args:
            url ([string]): 검색 URL
                ex ) : https://www.op.gg/champion/aatrox/statistics/top
                
            champ_num ([int]): 챔피언 번호
              ex ) : 266

            champ_line ([string]): 챔피언 가는 라인 대문자
              ex ) : "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"

        Returns:
            [json]: 룬
            ex ) : {0: {'Style': '8000.png',
                        'Keystone': '8010.png', 
                        'Substyle': '8400.png', 
                        'PickPercentage': '70.94', 
                        'WinRate': '51.65', 
                        'Detail': {0: {' ...
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            result_dict = {}

            # 이미지 정규식
            pattern = "([-\w]+\.(?:jpg|gif|png|jpeg))"

            url += "/rune"

            html = \
              self.read_html(url)

            div = html.find("div", class_="champion-box-content")
            
            li = div.find_all("li")

            for i in range(len(li) - 1):

                # 룬 이미지 추출
                # 룬 스타일 추출
                result_dict[i] = {}
                images_list = li[i].find_all("img")

                for j in range(len(images_list)):
                    img_src = images_list[j]["src"]
                    img_class = images_list[j]["class"]
                    item_image = re.search(pattern, img_src).group()
                    item_image = int(item_image.split(".")[0])

                    run_style = img_class[1].split("--")[-1].capitalize()
                    result_dict[i][run_style] = item_image

                # 픽률
                winrate = \
                  li[i].find_all("div", class_="champion-stats__filter_item_value--winrate")

                for j in range(len(winrate)):
                    result_dict[i]["PickPercentage"] = \
                      float(
                        winrate[j].find("b").get_text().replace("%", "")
                      )

                # 승률
                winrate = \
                  li[i].find_all("div", class_="champion-stats__filter_item_value--pickrate")
                  
                for j in range(len(winrate)):
                    result_dict[i]["WinRate"] = \
                      float(
                        winrate[j].find("b").get_text().replace("%", "")
                      )

            # 룬 URL 제작
            self.RUNE_AJAX_URL = \
              "https://www.op.gg/champion/ajax/statistics/runeList/championId={}&position={}&primaryPerkId={}&subPerkStyleId={}&"
            # "https://www.op.gg/champion/ajax/statistics/runeList/championId=266&position=MID&primaryPerkId=8112&subPerkStyleId=8300&"

            for k in result_dict.keys():
                primary_perkid = result_dict[k]["Keystone"]
                sub_perk_style_id = result_dict[k]["Substyle"]
            
                URL = self.RUNE_AJAX_URL.format(champ_num, # 챔피언 번호
                                                champ_line, # 라인 > "MID"
                                                primary_perkid, # 룬
                                                sub_perk_style_id ) # 룬
                

                html = self.read_html(URL)
                sleep(1)

                tr = html.find("tbody").find_all("tr")

                result_dict[k]["Detail"] = {}

                # 룬
                for i in range(len(tr)):
                    result_dict[k]["Detail"][i] = {}
                    div = tr[i].find_all("div", class_="perk-page__item--active")
                    for j in range(len(div)):
                        img_src = div[j].find("img")["src"]
                        img_name = div[j].find("img")["alt"]
                        rune_image = re.search(pattern, img_src).group()
                        rune_image = int(rune_image.split(".")[0])
                        result_dict[k]["Detail"][i][img_name] = rune_image

                # 룬 etc
                div = html.find("tbody").find_all("div", class_="fragment-page")
                for i in range(len(div)-1):
                    il = []
                    iln = []
                    img = div[i].find_all("img", class_="active")
                    for j in range(len(img)):
                        img_src = img[j]["src"]
                        img_name = img[j]["alt"]
                        rune_image = re.search(pattern, img_src).group()
                        rune_image = int(rune_image.split(".")[0])
                        iln.append(img_name)
                        il.append(rune_image)
                    result_dict[k]["Detail"][i]["EtcRuneImage"] = il
                    result_dict[k]["Detail"][i]["EtcRuneName"] = iln


                # 룬 픽률, 승률, 픽수
                td_pickrate = \
                  html.find("tbody").find_all("td", class_="champion-stats__table__cell--pickrate")

                td_winrate = \
                  html.find("tbody").find_all("td", class_="champion-stats__table__cell--winrate")

                for i in range(len(td_pickrate)):
                  pick = \
                    td_pickrate[i].get_text().replace(" ", "").strip().split("%")

                  result_dict[k]["Detail"][i]["PickPercentage"] = \
                    float(
                      pick[0]
                    )
                    
                  result_dict[k]["Detail"][i]["PickCount"] = \
                    int(
                      pick[1].replace(",", "")
                    )

                  result_dict[k]["Detail"][i]["WinRate"] = \
                    float(
                      td_winrate[i].get_text().replace("%", "")
                    )
                    
            result_dict["champNum"] = champ_num
            result_dict["champLine"] = champ_line

            return result_dict
    
        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



