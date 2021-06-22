"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/garen/statistics/top
  OpggStatisticsDetail 클래스 정의 코드

"""


import re
from opgg_statistics import OpggStatistics


class OpggStatisticsDetail(OpggStatistics):




    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | OpggStatisticsDetail > run")

        # 챔피언 통계 
        self.OPGG_URL = "https://www.op.gg/champion/statistics"

        # 챔피언 BAN 통계
        self.OPGG_TREND_CHAMP_BAN = "https://www.op.gg/champion/ajax/statistics/trendChampionList/type=banratio&"




    def champion_line(self):
        """
            챔피언이 가는 라인을 찾아서
           dict 형식으로 return 합니다.
        Returns:
            [dict]]: 아래와 같은 형식으로 리턴 합니다.
                {'aatrox': ['top', 'mid'], 'ahri': ['mid'], ... }
        """

        self.logger.info("FUC | OpggStatisticsDetail.champion_line > run")

        try:
            # 결과 저장 리스트
            result_dict = {}

            ## html 읽기
            html = self.read_html(self.OPGG_URL)
            
            ## 티어 챔피언 정보 tag 리스트
            champion_info_list = html.find("div", class_="champion-index__champion-list"
                                    ).find_all("a")


            for n in range(len(champion_info_list)):

                lt = []

                champion_name = champion_info_list[ n
                                ].find("div", class_="champion-index__champion-item__name"
                                ).get_text().lower()
                
                # 누누 예외 처리
                if champion_name == 'nunu & willump':
                    champion_name = 'nunu'

                champion_line = champion_info_list[ n
                                ].find("div", class_="champion-index__champion-item__positions"
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
            self.logger.error("FUC | OpggStatisticsDetail.champion_line  > ")




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

        self.logger.info("FUC | OpggStatisticsDetail.champion_line_url > run")

        try:
            result_list = []

            champion_line = self.champion_line()


            for k, value_list in champion_line.items():
                for vl in value_list:
                    URL = "https://www.op.gg/champion/{}/statistics/{}".format(k, vl)
                    result_list.append(URL)

            return result_list

        except:
            self.logger.error("FUC | OpggStatisticsDetail.champion_line_url  > ")




    def champion_detail_synthesize(self):

        self.logger.info("FUC | OpggStatisticsDetail.champion_detail_synthesize > run")

        # 결과 딕셔너리
        result_dict = {}

        html = self.read_html("https://www.op.gg/champion/aatrox/statistics/top")
        tbody = html.find_all("tbody")

        # 카운터 챔피언
        counter_champion = tbody[0].find_all("td", class_="champion-stats-header-matchup__table__champion")
        counter_winrate = tbody[0].find_all("td", class_="champion-stats-header-matchup__table__winrate")

        result_dict["CounterChampion"] = {}

        for i in range(len(counter_champion)):
          cc = counter_champion[i].get_text().strip() # 카운터 챔피언 
          cw = counter_winrate[i].find("b").get_text().replace("%", "") # 카운터 챔피언  승률
          result_dict["CounterChampion"][cc] = cw


        # 상대하기 쉬운 챔피언
        counter_champion = tbody[1].find_all("td", class_="champion-stats-header-matchup__table__champion")
        counter_winrate = tbody[1].find_all("td", class_="champion-stats-header-matchup__table__winrate")

        result_dict["EasyChampion"] = {}

        for i in range(len(counter_champion)):
          cc = counter_champion[i].get_text().strip() # 카운터 챔피언 
          cw = counter_winrate[i].find("b").get_text().replace("%", "") # 카운터 챔피언  승률
          result_dict["EasyChampion"][cc] = cw


        # 챔피언 스펠
        result_dict["Spell"] = {}
        result_dict["Spell"][0] = {}
        result_dict["Spell"][1] = {}
        result_dict["Spell"][0]["SpellImage"] = []
        result_dict["Spell"][1]["SpellImage"] = []

        # 챔피언 spell 이미지 추출
        spell_list = tbody[2].find_all("li", class_="champion-stats__list__item")

        # 이미지 정규식
        pattern = "([-\w]+\.(?:jpg|gif|png|jpeg))"

        for i in range(len(spell_list)):
            spell_image = re.search(pattern, spell_list[i].img["src"]).group()
            if i//2 == 0:
                result_dict["Spell"][0]["SpellImage"].append(spell_image)
            else:
                result_dict["Spell"][1]["SpellImage"].append(spell_image)
        
        # spell 픽률
        spell_pick_list = tbody[2].find_all("td", class_="champion-overview__stats champion-overview__stats--pick")

        for i in range(len(spell_pick_list)):
            result_dict["Spell"][i]["PickPercentage"] = \
              spell_pick_list[i].find("strong").get_text().replace("%", "")

            result_dict["Spell"][i]["PickCount"] = \
              spell_pick_list[i].find("span").get_text()


        # spell 승률
        spell_win_list = tbody[2].find_all("td", class_="champion-overview__stats champion-overview__stats--win")
        for i in range(len(spell_win_list)):
            result_dict["Spell"][i]["WinRate"] = \
              spell_win_list[i].find("strong").get_text().replace("%", "")

        # 챔피언 스킬
        result_dict["SkillBuild"] = []

        skill_list = tbody[4].find_all("td")
        for i in range(len(skill_list)):
            skill = skill_list[i].get_text().strip()
            result_dict["SkillBuild"].append(skill)

        # 챔피언 게임시작 아이템
        result_dict["ItemBuild"] = {}
        result_dict["ItemBuild"]["StarterItems"] = {}
        result_dict["ItemBuild"]["RecommendedBuilds"] = {}
        result_dict["ItemBuild"]["Boots"] = {}

        item_list = tbody[5].find_all("tr")
        for i in range(len(item_list)):

            il = [] # 아이템 이미지 저장 리스트 

            if i in range(1): # 시작 아이템
                dict_tmp_name = "StarterItems"
            if i in range(2, 6): # 추천 빌드
                dict_tmp_name = "RecommendedBuilds"
            if i in range(7, 9): # 신발
                dict_tmp_name = "Boots"
                
            result_dict["ItemBuild"][dict_tmp_name][i] = {}

            for tag in item_list[i].find_all("img"): # 이미지 리스트에 넣기
                item_image = re.search(pattern, tag["src"]).group()
                # blet.png 이미지 제거
                if item_image == "blet.png": continue
                il.append(item_image)

            result_dict["ItemBuild"][dict_tmp_name][i]["Images"] = il # 이미지 리스트

            # 픽률
            result_dict["ItemBuild"][dict_tmp_name][i]["PickPercentage"] = \
              item_list[i].find("strong").get_text().replace("%", "")

            # 픽 횟수
            result_dict["ItemBuild"][dict_tmp_name][i]["PickCount"] = \
              item_list[i].find("span").get_text()

            # 픽 승률
            result_dict["ItemBuild"][dict_tmp_name][i]["WinRate"] = \
              item_list[i].find_all("strong")[1].get_text()


        self.html_code_save(
          item_list[2],
          "champion_detail_synthesize.txt"
        )

        # 룬 헤더
        tbody[6]

        # 첫번째 룬 정보
        tbody[7]

        # 두번째 룬 정보
        tbody[8]

        # 트렌드 그래프
        html.find("div", class_="champion-box-content")

        return result_dict



if __name__ == '__main__':
    a = OpggStatisticsDetail()
    print(
      a.champion_detail_synthesize()
    )
