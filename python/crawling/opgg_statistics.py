"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/statistics
  OpggStatistics 클래스 정의 코드

"""

from opgg_main import Opgg



class OpggStatistics(Opgg):



    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | OpggStatistics > run")

        # 챔피언 통계 
        self.OPGG_URL = "https://www.op.gg/champion/statistics"

        # 챔피언 BAN 통계
        self.OPGG_TREND_CHAMP_BAN = "https://www.op.gg/champion/ajax/statistics/trendChampionList/type=banratio&"




    def champion_statistics_info(self):
        """챔피언 라인별 티어, 승률, 픽률, 정보
           리스트 형으로 출력

        Returns:
            [list]: 챔피언 통계 결과 리스트 

            ex ) : [['11.12', '1', 'stay', '0', 'TOP', 'Sett', 'Top, Support, Middle', '51.03', '16.34', '1'],
                    ['11.12', '2', 'stay', '0', 'TOP', 'Sylas', 'Middle, Top', '49.81', '12.39', '1'], ...
        """

        self.logger.info("FUC | OpggStatistics.champion_statistics_info > run")

        # 결과 저장 리스트
        result_list = []

        try:
            ## html 읽기
            html = self.read_html(self.OPGG_URL)

            # 크롤링 코드 확인
            # self.html_code_save(html, "find_champion_statistics_info.txt") 
            
            data_version = html.find("div", class_="champion-index__version"
                                    ).get_text(
                                    ).split(':'
                                    )[1].strip()

            for line in  ("TOP", "JUNGLE", "MID", "ADC", "SUPPORT"):

                ## 티어 챔피언 정보 tag 리스트
                champion_info_list= html.find("tbody", class_='tabItem champion-trend-tier-{}'.format(line)
                                      ).find_all('tr')

                for n in range(len(champion_info_list)):

                    # rank 순서
                    rank_num = champion_info_list[n].find("td", class_= "champion-index-table__cell "
                                                                      + "champion-index-table__cell--rank"
                                                  ).get_text()

                    # line 찾기
                    line_position = champion_info_list[n].find("a"
                                                        ).attrs["href"
                                                        ].split("/")[-1
                                                        ].upper()

                    # champion_name 찾기
                    champion_name = champion_info_list[n].find("div", class_="champion-index-table__name"
                                                        ).get_text() 

                    # 전 티어 순위 변동 상태
                    change_tier_state = champion_info_list[n].find("td", class_="champion-index-table__cell--change"
                                                            ).attrs['class'][2
                                                            ].split("--")[-1]

                    # 전 티어 순위 변동 값
                    change_tier_value =  champion_info_list[n].find("td", class_="champion-index-table__cell--change"
                                                            ).get_text(
                                                            ).strip()

                    # 승률
                    winning_rate = champion_info_list[n].find_all("td", class_= "champion-index-table__cell " 
                                                                              + "champion-index-table__cell--value")[0
                                                      ].get_text(
                                                      ).replace("%", "")

                    # 픽률
                    pick_rate = champion_info_list[n].find_all("td", class_= "champion-index-table__cell " 
                                                                           + "champion-index-table__cell--value")[1
                                                    ].get_text(
                                                    ).replace("%", "")

                    # tier 찾기
                    tier = champion_info_list[n].find_all("img")[-1
                                              ].attrs["src"
                                              ].split("-")[-1
                                              ].split(".")[0]

                    # 다른 라인
                    go_line = champion_info_list[n].find("div", class_="champion-index-table__position"
                                                  ).get_text(
                                                  ).replace("\t", ""
                                                  ).replace("\n", "")

                    # print(data_version, # 버전
                    #       rank_num, # 순위 번호
                    #       change_tier_state, # 순위 변화 상태
                    #       change_tier_value, # 순위 변화량
                    #       line_position, # 가는 라인
                    #       champion_name, # 챔피언 이름
                    #       go_line, # 챔피언이 가는 다른 라인
                    #       winning_rate, # 챔피언 승률
                    #       pick_rate, # 챔피언 픽률
                    #       tier # 티어
                    # )

                    # 결과 list에 저장
                    result_list.append([data_version,
                                        rank_num,
                                        change_tier_state,
                                        change_tier_value,
                                        line_position,
                                        champion_name,
                                        go_line,
                                        winning_rate,
                                        pick_rate,
                                        tier])

            return result_list

        except:
            self.logger.error("FUC | OpggStatistics.champion_statistics_info  > ")




    def champion_statistics_ban_info(self):
        """챔피언 라인별 밴률 정보
           리스트 형으로 출력

        Returns:
            [list]: 챔피언  밴 랭킹 결과 리스트

            ex ) : [['1', 'ALL', 'Samira', '63.98'],
                    ['2', 'ALL', 'Ezreal', '56.10'], ...
        """
  
        self.logger.info("FUC | OpggStatistics.champion_statistics_ban_info > run")

        # 결과 저장 리스트
        result_list = []

        try:
            ## html 읽기
            html = self.read_html(self.OPGG_TREND_CHAMP_BAN)

            # 크롤링 코드 확인
            # self.html_code_save(html, "champion_statistics_ban_info.txt")

            for line in ("ALL", "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"):

                css_selecter = "tabItem champion-trend-banratio-{}".format(line)
                ## 티어 챔피언 정보 tag 리스트
                champion_info_list= html.find("tbody", attrs={"class":css_selecter}
                                      ).find_all('tr')
                for n in range(len(champion_info_list)):

                    # rank 순서
                    rank_num = champion_info_list[n].find("td", class_= "champion-index-table__cell " 
                                                                      + "champion-index-table__cell--rank"
                                                  ).get_text()

                    # filter
                    line_filter = champion_info_list[n].find("a"
                                                        ).attrs["href"
                                                        ].split("/")[-1
                                                        ].upper()

                    # champion_name 찾기
                    champion_name = champion_info_list[n].find("div", class_="champion-index-table__name"
                                                        ).get_text() 

                    # 밴률
                    ban_rate = champion_info_list[n].find("td", class_="champion-index-table__cell--value"
                                                  ).get_text(
                                                  ).replace("%", "")

                    # print(
                    #    rank_num, # 번호
                    #    line_filter, # 라인 검색 필터
                    #    champion_name, #  챔피언 이름
                    #    ban_rate # 밴률
                    # )

                    # 결과 list에 저장
                    result_list.append([
                      rank_num,
                      line_filter,
                      champion_name,
                      ban_rate
                    ])

            return result_list

        except:
            self.logger.error("FUC | OpggStatistics.champion_statistics_ban_info  > ")



