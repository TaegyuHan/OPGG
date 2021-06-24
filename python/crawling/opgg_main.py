"""

  op.gg main 크롤링 코드 입니다.
  Opgg 클래스 정의 코드

"""

from bs4 import BeautifulSoup
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from log import log # 로그





class Opgg():



    def __init__(self):

        self.logger = log.make_logger("OPGG")
        self.logger.info("CLASS | Opgg > run")




    def read_html(self, url):
        """
            URL을 받아서 html을 bs4.BeautifulSoup
            type으로 변환해서 돌려줍니다.
        Args:
            URL ([String]]): "https://www.google.com"
        Returns:
            [class(bs4.BeautifulSoup)]: BeautifulSoup
        """

        self.logger.info("FUC | OPGG.read_html > run")

        # 접속 정보
        # hdr = { 'Accept-Language' : 'ko_KR,en;q=0.8' }

        try:
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            self.soup_html = soup
            return soup

        except:
            self.logger.error("FUC | OPGG.read_html > ")




    def html_code_save(self, html, file_name):
        """BeautifulSoup type의 html소스를 받아서
           txt 형태로 저장합니다.

        Args:
            [class(bs4.BeautifulSoup)]: BeautifulSoup
        """

        self.logger.info("FUC | OPGG.html_code_save > run")

        f = open(file_name, "w", -1, "utf-8")
        f.write(str(html))
        f.close()




