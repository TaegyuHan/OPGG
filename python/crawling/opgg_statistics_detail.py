"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/garen/statistics/top
  OpggStatisticsDetail 클래스 정의 코드

"""
import sys

from opgg_statistics import OpggStatistics


class OpggStatisticsDetail(OpggStatistics):




    def __init__(self):
        OpggStatistics.__init__(self) # 부모 생성자
        self.logger.info("CLASS | {} > run".format(self.__class__.__name__))




    def champion_line(self):
        """
            챔피언이 가는 라인을 찾아서
           dict 형식으로 return 합니다.
        Returns:
            [dict]]: 아래와 같은 형식으로 리턴 합니다.
                {'aatrox': ['top', 'mid'], 'ahri': ['mid'], ... }
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            # 결과 저장 리스트
            result_dict = {}

            ## html 읽기
            html = self.read_html(self.OPGG_URL)
            
            ## 티어 챔피언 정보 tag 리스트
            champion_info_list = \
              html.find("div", class_="champion-index__champion-list").find_all("a")


            for n in range(len(champion_info_list)):

                lt = []

                champion_name = \
                  champion_info_list[n].find("div", class_="champion-index__champion-item__name"
                                      ).get_text().lower()
                
                # 누누 예외 처리
                if champion_name == 'nunu & willump':
                    champion_name = 'nunu'

                champion_line = \
                  champion_info_list[n].find("div", class_="champion-index__champion-item__positions"
                    ).find_all("div", class_="champion-index__champion-item__position")

                # 챔피언의 라인 넣기
                # 1개 이상이 나올 수 있어서 전부 찾아줌
                for cl in champion_line:
                    line = cl.get_text()
                    if line == "Top": lt.append("top")
                    if line == "Middle": lt.append("mid")
                    if line == "Jungle": lt.append("jungle")
                    if line == "Support": lt.append("support")
                    if line == "Bottom": lt.append("adc")

                result_dict[champion_name] = lt

            return result_dict

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))




    def champion_line_url(self):
        """ 
            챔피언의 라인별로 URL을 생성 후
            list type으로 return 합니다.

        Returns:
            [list]: 아래와 같은 형식으로 리턴 합니다.
                ['https://www.op.gg/champion/aatrox/statistics/top',
                 'https://www.op.gg/champion/ahri/statistics/mid',
                    ... ]
        """

        self.logger.info("FUC | {} > run".format(sys._getframe().f_code.co_name))

        try:
            result_list = []

            champion_line = self.champion_line()


            for k, value_list in champion_line.items():
                for vl in value_list:
                    URL = "https://www.op.gg/champion/{}/statistics/{}".format(k, vl)
                    result_list.append(URL)

            return result_list

        except:
            self.logger.error("FUC | {} > error".format(sys._getframe().f_code.co_name))


# if __name__ == '__main__':
#     a = OpggStatisticsDetail()
#     print(a.champion_line_url())