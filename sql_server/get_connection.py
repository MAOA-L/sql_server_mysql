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

server = '127.0.0.1'  # 数据库服务器名称或IP
user = 'sa'  # 用户名
password = '13486059134Chen'  # 密码
database = 'new_con'  # 数据库名称
charset = 'utf8'
conn = pymssql.connect(host=server, user=user, password=password, database=database, charset=charset)

cursor = conn.cursor()


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

    def get_conn(self):
        self.close_conn()
        if not self.conn:
            _current_time = time.time()
            self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password,
                                        database=self.database,
                                        charset=self.charset)
            self.close_at = _current_time + self.conn_age * 1000
        return self.conn

    def close_conn(self):
        if self.conn and time.time() > self.close_at:
            self.conn.close()


connection = SqlServer()

if __name__ == '__main__':
    conn = connection.get_conn()
    sql = "SELECT grxx_tb.cardnum, grxx_tb.name, group_tb.groupshortname, grxx_tb.REGSTATE" \
          " FROM grxx_tb, group_tb WHERE grxx_tb.groupid= group_tb.groupid AND grxx_tb.groupid= 2 " \
          "AND regstate = 0 ORDER BY grxx_tb.groupid"
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor:
        print([i.encode("latin-1").decode("gbk") if isinstance(i, str) else i for i in row])
