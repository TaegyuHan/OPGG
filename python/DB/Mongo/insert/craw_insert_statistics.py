# -*- coding: utf-8 -*-

"""
   DB : MongoDB
   Database : opgg
   Collection : championStatisticsInfo

   데이터 입력 code
"""


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mongo_config import MongoDB_DB

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from log import log # 로그
from crawling.opgg_statistics import OpggStatistics

crawling = OpggStatistics()
crawling.