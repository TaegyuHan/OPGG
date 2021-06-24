""" 
    MySQL 연결 core code

"""

import mysql.connector

import sys
sys.path.append("../../")
from log import log # 로그



class MySQL_DB():




    def __init__(self):

        # 로그 생성
        self.logger = log.make_logger("MySQL_DB")
        self.logger.info("CLASS | MySQL_DB > run")

        # DB 연결
        try:
            self.DB = mysql.connector.connect(
                            host="127.0.0.1",
                            user="root",
                            password="",
                            database="opgg"
                    )
                    
            self.logger.info("CLASS | DB connect | > success")

        except:
            self.logger.error("CLASS | DB connect | > error")



    def insert(self, sql, val):
        """DB INSERT 함수
           SQL isnert문을 받아서 실행 합니다.

        Args:
            sql ([string (SQL)]): insert 쿼리문
                    ex) : "INSERT INTO customers (name, address) 
                           VALUES (%s, %s)"

            val ([tuple]): tuple value
                    ex) : ("John", "Highway 21")

        """

        self.logger.info("FUN | INSER | > run")

        try:
            mycursor = self.DB.cursor()
            mycursor.execute(sql, val)
            self.DB.commit()

            self.logger.info("FUN | SQL | {} | > run".format(sql))
            self.logger.info("FUN | INSERT | > success")

        except:
            self.logger.error("FUN | INSERT | > error")




    def select(self, sql):
        """DB SELECT 함수
           SQL select문을 받아서 실행 합니다.

        Args:
            sql ([string (SQL)]): select 쿼리문
                    ex) : "SELECT * FROM customers"

        Returns:
            [list]: SQL 결과 list
                    ex) : [ ('John', 'Highway 21'),
                            ('John', 'Highway 21') ... ]
        """

        self.logger.info("FUN | SELECT | > run")

        try:
            mycursor = self.DB.cursor()
            mycursor.execute(sql)
            
            self.logger.info("FUN | SQL | {} | > run".format(sql))
            self.logger.info("FUN | SELECT | > success")

            return mycursor
            
        except:
            self.logger.error("FUN | SELECT | > error")




    def delete(self, sql):
        """DB DELETE 함수
           SQL delete문을 받아서 실행 합니다.

        Args:
            sql ([string (SQL)]): delete 쿼리문
                    ex) : "DELETE FROM customers
                           WHERE address = 'Mountain 21'"
        """
        
        self.logger.info("FUN | DELETE | > run")

        try:
            mycursor = self.DB.cursor()
            mycursor.execute(sql)
            self.DB.commit()

            self.logger.info("FUN | SQL | {} | > run".format(sql))
            self.logger.info("FUN | DELETE | > success")

        except:
            self.logger.error("FUN | DELETE | > error")




    def update(self, sql):
        """DB DELETE 함수
           SQL update문을 받아서 실행 합니다.

        Args:
            sql ([string (SQL)]): update 쿼리문
                    ex) : "UPDATE customers
                           SET address = 'Canyon 123'
                           WHERE address = 'Valley 345'" 
        """

        self.logger.info("FUN | UPDATE | > run")

        try:
            mycursor = self.DB.cursor()
            mycursor.execute(sql)
            self.DB.commit()
            
            self.logger.info("FUN | SQL | {} | > run".format(sql))
            self.logger.info("FUN | UPDATE | > success")

        except:
            self.logger.error("FUN | UPDATE | > error")



