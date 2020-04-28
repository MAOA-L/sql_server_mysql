# -*- coding: utf-8 -*-
"""
 @Time    : 19/12/6 11:11
 @Author  : CyanZoy
 @File    : get_connection.py
 @Software: PyCharm
 @Describe: 
 """
import time

import pymssql
import pyodbc

from log import logger

# server = 'server'  # 数据库服务器名称或IP
server = '127.0.0.1'  # 数据库服务器名称或IP
user = 'sa'  # 用户名
# password = 'sa'  # 密码
password = '13486059134Chen'  # 密码
database = 'con1'  # 数据库名称
# database = 'new_con'  # 数据库名称
charset = 'utf8'
# conn = pymssql.connect(host=server, user=user, password=password, database=database, charset=charset)
#
# cursor = conn.cursor()


class SqlServer:
    """

    """

    def __init__(self):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = None
        self.close_at = None
        self.conn_age = 20
        self.conn_success = self._test_conn()

    def _test_conn(self):
        try:
            self.get_conn()
            return True
        except Exception as ex:
            logger.error("sqlserver连接失败")
            logger.info(ex)

    def get_conn(self):
        self.close_conn()
        if not self.conn:
            _current_time = time.time()
            # self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password,
            #                             database=self.database, charset=self.charset)
            self.conn = pyodbc.connect("DRIVER={SQL Server};SERVER=127.0.0.1;UID=sa;PWD=13486059134Chen;DATABASE=con1")
            self.close_at = _current_time + self.conn_age * 1000
        return self.conn

    def close_conn(self):
        if self.conn and time.time() > self.close_at:
            self.conn.close()


connection = SqlServer()

if __name__ == '__main__':
    if connection.conn_success:
        conn = connection.get_conn()
        sql = "SELECT GRXX_TB.cardnum, GRXX_TB.name, group_tb.groupshortname, GRXX_TB.REGSTATE" \
              " FROM GRXX_TB, group_tb WHERE GRXX_TB.groupid= group_tb.groupid ORDER BY GRXX_TB.groupid"
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor:
            logger.info([i if isinstance(i, str) else i for i in row])
    else:
        logger.error("连接未成功")
