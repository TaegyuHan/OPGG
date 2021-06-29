"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/{}/statistics/{}/item
  OpggStatisticsDetailItem 클래스 정의 코드

"""


import re
import sys
import os


sys.path.append(os.path.dirname(__file__))
from opgg_statistics_detail import OpggStatisticsDetail


class OpggStatisticsDetailItem(OpggStatisticsDetail):




    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))




    def champion_detail_item(self, url):
        """OPGG 챔피언 세부 아이템 page 정보

        Args:
            url ([string]): 검색 URL
                ex ) : https://www.op.gg/champion/aatrox/statistics/top
                
          Returns:
              [json]: 아이템
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
            # 결과 딕셔너리
            result_dict = {}

            champ_name = url.split("/")[-3]
            champ_line = url.split("/")[-1]

            url += "/item"

            html = \
              self.read_html(url)

            # 이미지 정규식
            pattern = "([-\w]+\.(?:jpg|gif|png|jpeg))"


            for k in range(0, 4):
                
                thead_num = k
                tbody_num = k + 2

                # 아이템 title
                title = \
                  html.find_all("thead")[thead_num].find("th", class_="champion-stats__table__header--title"
                  ).get_text().replace(" ", "")

                result_dict[title] = {}

                # 아이템 이미지
                # 핵심 빌드, 시작 아이템 list
                if tbody_num in (2, 4):
                    ul = html.find_all("tbody")[tbody_num].find_all("ul", class_="champion-stats__list")

                    for i in range(len(ul)):
                        result_dict[title][i] = {}
                        img = ul[i].find_all("img")
                        il = []

                        for j in range(len(img)):
                            img_src = img[j]["src"]
                            item_image = re.search(pattern, img_src).group()
                            if item_image == "blet.png": continue

                            item_image = int(item_image.split(".")[0])
                            il.append(item_image)

                        result_dict[title][i]["item"] = il
                
                # 신발, 아이템 list
                if tbody_num in (3, 5):
                    ul = html.find_all("tbody")[tbody_num].find_all("div", class_="champion-stats__single__item")

                    for i in range(len(ul)):
                        result_dict[title][i] = {}
                        img = ul[i].find_all("img")
                        il = []

                        for j in range(len(img)):
                            img_src = img[j]["src"]
                            item_image = re.search(pattern, img_src).group()
                            if item_image == "blet.png": continue

                            item_image = int(item_image.split(".")[0])
                            il.append(item_image)

                        result_dict[title][i]["item"] = il

                # 픽률 , 픽수
                td1 = \
                  html.find_all("tbody")[tbody_num
                  ].find_all("td", class_="champion-stats__table__cell champion-stats__table__cell--pickrate")

                # 픽 승률
                td2 = \
                  html.find_all("tbody")[tbody_num
                  ].find_all("td", class_="champion-stats__table__cell champion-stats__table__cell--winrate")

                for i in range(len(td1)):
                    # 픽률, 픽수
                    if tbody_num in (2, 4, 5):
                        pick1 = \
                          td1[i].get_text().strip().replace(" ", "").replace("\t", "").split("\n")

                    if tbody_num == 3:
                        pick1 = \
                            td1[i].get_text().strip().replace(" ", "").replace("\t", "").split("%")

                    # 픽 승률
                    pick2 = td2[i].get_text().replace("%", "")

                    result_dict[title][i]["PickPercentage"] = \
                      float(
                        pick1[0].replace("%", "")
                      )

                    result_dict[title][i]["PickCount"] = \
                      int(
                        pick1[1].replace(",", "")
                      )

                    result_dict[title][i]["WinRate"] = \
                      float(
                        pick2
                      )

            result_dict["champName"] = champ_name
            result_dict["champLine"] = champ_line

            return result_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))



