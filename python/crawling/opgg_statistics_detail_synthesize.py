"""

  op.gg 크롤링 코드
  URL : https://www.op.gg/champion/garen/statistics/top
  OpggStatisticsDetailSynthesize 클래스 정의 코드

"""


import re
from opgg_statistics_detail import OpggStatisticsDetail


class OpggStatisticsDetailSynthesize(OpggStatisticsDetail):




    def __init__(self):
        super().__init__() # 부모 생성자
        self.logger.info("CLASS | OpggStatisticsDetailSynthesize > run")




    def champion_detail_synthesize(self):
        """OPGG 챔피언 세부 종합 page 정보

        Returns:
            [json]: 세부 정보
            ex ) : {'CounterChampion': {'Heimerdinger': '46.04',
                                        'Nocturne': '46.33',
                                        'Kled': '46.70'},
                    'EasyChampion': {'Lucian': ... }
        """

        self.logger.info("FUC | OpggStatisticsDetailSynthesize.champion_detail_synthesize > run")

        try:
            # 결과 딕셔너리
            result_dict = {}

            html = \
              self.read_html("https://www.op.gg/champion/aatrox/statistics/top")

            tbody = html.find_all("tbody")

            # 카운터 챔피언
            counter_champion = \
              tbody[0].find_all("td", class_="champion-stats-header-matchup__table__champion")

            counter_winrate = \
              tbody[0].find_all("td", class_="champion-stats-header-matchup__table__winrate")

            result_dict["CounterChampion"] = {}

            for i in range(len(counter_champion)):
              cc = counter_champion[i].get_text().strip() # 카운터 챔피언 
              cw = counter_winrate[i].find("b").get_text().replace("%", "") # 카운터 챔피언  승률
              result_dict["CounterChampion"][cc] = cw


            # 상대하기 쉬운 챔피언
            counter_champion = \
              tbody[1].find_all("td", class_="champion-stats-header-matchup__table__champion")

            counter_winrate = \
              tbody[1].find_all("td", class_="champion-stats-header-matchup__table__winrate")

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
            spell_pick_list = \
              tbody[2].find_all("td", class_="champion-overview__stats champion-overview__stats--pick")

            for i in range(len(spell_pick_list)):
                result_dict["Spell"][i]["PickPercentage"] = \
                  spell_pick_list[i].find("strong").get_text().replace("%", "")

                result_dict["Spell"][i]["PickCount"] = \
                  spell_pick_list[i].find("span").get_text()


            # spell 승률
            spell_win_list = \
              tbody[2].find_all("td", class_="champion-overview__stats champion-overview__stats--win")
            for i in range(len(spell_win_list)):
                result_dict["Spell"][i]["WinRate"] = \
                  spell_win_list[i].find("strong").get_text().replace("%", "")

            # 챔피언 스킬
            result_dict["SkillBuild"] = {}
            result_dict["SkillBuild"]["Sequence"] = []
            
            # 스킬 순서
            skill_list = tbody[4].find_all("td")
            for i in range(len(skill_list)):
                skill = skill_list[i].get_text().strip()
                result_dict["SkillBuild"]["Sequence"].append(skill)
            
            # 스킬 픽률
            result_dict["SkillBuild"]["PickPercentage"] = \
              tbody[3].find("td", class_="champion-overview__stats--pick"
              ).find("strong").get_text().replace("%", "")

            # 스킬 픽 수
            result_dict["SkillBuild"]["PickCount"] = \
              tbody[3].find("td", class_="champion-overview__stats--pick"
              ).find("span").get_text().replace("%", "")              

            # 스킬 승률
            result_dict["SkillBuild"]["WinRate"] = \
              tbody[3].find("td", class_="champion-overview__stats--win"
              ).find("strong").get_text().replace("%", "")



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

                # 이미지 추출
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



            # 룬 헤더
            result_dict["Rune"] = {}
            result_dict["Rune"][0] = {}
            result_dict["Rune"][1] = {}

            # 룬 헤더 이미지
            rune_img_list = \
              tbody[6].find_all("div", class_="champion-stats-summary-rune-image")
            for i in range(len(rune_img_list)):
                il = []
                for img in rune_img_list[i].find_all("img"):
                    rune_image = re.search(pattern, img["src"]).group()
                    il.append(rune_image)
                result_dict["Rune"][i]["HeaderInfoImage"] = il

            # 룬 헤더 이름, 픽률, 승률
            rune_name = \
              tbody[6].find_all("div", class_="champion-stats-summary-rune__name")
            rune_rate = \
              tbody[6].find_all("div", class_="champion-stats-summary-rune__rate")

            for i in range(len(rune_name)):
                result_dict["Rune"][i]["HeaderRuneName"] = \
                  rune_name[i].get_text()
                  
                result_dict["Rune"][i]["HeaderPickPercentage"] = \
                  rune_rate[i].find("strong").get_text().replace("%", "")
                  
                result_dict["Rune"][i]["HeaderWinRate"] = \
                  rune_rate[i].find_all("span")[2].get_text().replace("%", "")

            # 첫번째 룬 정보 > 7
            # 두번째 룬 정보 > 8
            for n in range(7,9):
                
                if n == 7: m = 0
                if n == 8: m = 1

                td = tbody[n].find_all("td", class_="champion-overview__data")
                result_dict["Rune"][m]["RuneChoice"] = {}
                
                for i in range(len(td)):
                    result_dict["Rune"][m]["RuneChoice"][i] = {}
                    div = td[i].find_all("div", class_="perk-page__item--active")
                    for j in range(len(div)):
                        img_src = div[j].find("img")["src"]
                        img_name = div[j].find("img")["alt"]
                        rune_image = re.search(pattern, img_src).group()
                        result_dict["Rune"][m]["RuneChoice"][i][img_name] = rune_image

                # 룬 etc
                div = tbody[n].find_all("div", class_="fragment-page")
                for i in range(len(div)):
                    il = []
                    iln = []
                    img = div[i].find_all("img", class_="active")
                    for j in range(len(img)):
                        img_src = img[j]["src"]
                        img_name = img[j]["alt"]
                        rune_image = re.search(pattern, img_src).group()
                        iln.append(img_name)
                        il.append(rune_image)
                    result_dict["Rune"][m]["RuneChoice"][i]["EtcRuneImage"] = il
                    result_dict["Rune"][m]["RuneChoice"][i]["EtcRuneName"] = iln

                # 룬 픽률, 승률, 픽수
                td = tbody[n].find_all("td", class_="champion-overview__stats")
                for i in range(len(td)):
                  result_dict["Rune"][m]["RuneChoice"][i]["PickPercentage"] = \
                    td[i].find_all("strong")[0].get_text().replace("%", "")

                  result_dict["Rune"][m]["RuneChoice"][i]["PickCount"] = \
                    td[i].find_all("span")[1].get_text()

                  result_dict["Rune"][m]["RuneChoice"][i]["WinRate"] = \
                    td[i].find_all("strong")[1].get_text().replace("%", "")


            # 트렌드 그래프
            # html.find("div", class_="champion-box-content")

            return result_dict

        except:
            self.logger.error("FUC | OpggStatisticsDetailSynthesize.champion_detail_synthesize  > ")



    