

def champ_num_line(url, cursor_find):
    """URL을 받아서 챔피언의 번호를
       반환 하는 함수

    Args:
        url ([string]): 챔피언 검색 URL
              ex ) : https://www.op.gg/champion/aatrox/statistics/top/

        cursor_find ([class]): Mongo DB 연결 
              type : <class 'pymongo.collection.Collection'>

    Returns:
        [string]: champ_number > 챔피언 번호 
                    ex ) : 266
                     
                  champ_line > 챔피언 가는 라인
                    ex ) : TOP

    """

    champ_line = url.split("/")[-1].upper()
    champ_name = url.split("/")[-3
    ].capitalize().replace("'", "").replace(".", "").replace(" ", "")

    champ_name_change = {
        "Aurelionsol":"AurelionSol",
        "Drmundo":"DrMundo",
        "Jarvaniv":"JarvanIV",
        "Kogmaw":"KogMaw",
        "Leesin":"LeeSin",
        "Masteryi":"MasterYi",
        "Missfortune":"MissFortune",
        "Reksai":"RekSai",
        "Tahmkench":"TahmKench",
        "Twistedfate":"TwistedFate",
        "Wukong" : "WuKong", # 오공 json 데이터 없음
        "Xinzhao":"XinZhao",
    }
    
    # 챔피언 이름 중간 소문자 대문자로 변경
    for key, val in champ_name_change.items():
        if key == champ_name:
            champ_name = val

    # 챔피언 번호 추출
    for dict in cursor_find.find({"champName":champ_name}):
        champ_number = dict["data"][champ_name]["key"]

    # 예외 처리 오공 json 데이터 없음
    # 따라서 직접 넣어줌
    if champ_name == "WuKong":
        champ_number = 62
    

    return champ_number, champ_line




        