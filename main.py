# -*- coding: utf-8 -*-
"""
 @Time    : 19/12/7 9:29
 @Author  : CyanZoy
 @File    : main.py
 @Software: PyCharm
 @Describe:
 """
import json
import time
from urllib.parse import urlencode

import requests
from pymssql import connect

from sql_server.get_connection import connection


class ApiRequest:
    @staticmethod
    def post(url, data, headers=None):
        try:
            p_rep = requests.post(url=url, data=data, headers=headers).json()
        except requests.exceptions.ConnectionError as ex:
            print(f"===登录连接失败===={ex}")
        else:
            return p_rep


class Login:
    def __init__(self):
        self.phone = 13905740095
        self.way = 3
        self.source = 2  # 1 pc   2 app
        self.code = 181001
        # self.login_url = 'http://127.0.0.1/v1/auth/login/'
        self.login_url = 'https://snpctest.zhijiasoft.com/v1/auth/login/'
        # self.login_url = 'https://snpc.zhijiasoft.com/v1/auth/login/'

    def get_token(self):
        p_rep = ApiRequest.post(url=self.login_url, data=self._get_data())
        token = self.get_arg(p_rep, "data", "user_info", "token")
        print(f"获取token--{token[:10]}...")
        return token

    def get_arg(self, data, *args):
        _temp_data = data
        for i in args:
            _temp_data = _temp_data.get(i) if _temp_data else None

        return _temp_data

    def _get_data(self):
        return {
            "mobile_phone": self.phone,
            "way": self.way,
            "source": self.source,
            "code": self.code,
            "login_url": self.login_url,
        }

    def __getitem__(self, item):
        return {
            "mobile_phone": self.phone,
            "way": self.way,
            "source": self.source,
            "code": self.code,
            "login_url": self.login_url,
        }.get(item)


class DataTransmit:
    def __init__(self):
        self.t = None
        self.keys = {
            "get_staff_info_sql": ["card_num", "username", "group_name", 'present', 'group_id']
        }
        self.get_staff_info_sql = "SELECT grxx_tb.cardnum, grxx_tb.name, group_tb.groupshortname, " \
                                  "grxx_tb.REGSTATE,group_tb.groupid FROM grxx_tb, group_tb " \
                                  "WHERE grxx_tb.groupid= group_tb.groupid ORDER BY grxx_tb.groupid"
        self.connection = connection
        self.close_at = time.time()

    def _get_token(self):
        if self.t and time.time() - self.close_at < 3600000:
            self.close_at = time.time()
            return self.t
        token = AppLogin.get_token()
        self.t = token
        return token

    @property
    def token(self):
        return self._get_token()

    def get_sql_server_data(self):
        conn = self.connection.get_conn()
        if conn:
            cursor = self._execute(conn, self.get_staff_info_sql)
            result = []
            for row in cursor:
                result.append([i.encode("latin-1").decode("gbk") if isinstance(i, str) else i for i in row])
            print(f"获取人员数据{result}")
            return result
        else:
            return None

    def _execute(self, conn: connect, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor

    def trans_to_9511(self, data, headers=None):
        # _url = 'http://127.0.0.1/v1/app/conference/staff/createOrUpdateConferenceUserInfo/'
        _url = 'https://snpctest.zhijiasoft.com/v1/app/conference/staff/createOrUpdateConferenceUserInfo/'
        # _url = 'https://snpc.zhijiasoft.com/v1/app/conference/staff/createOrUpdateConferenceUserInfo/'
        res = ApiRequest.post(url=_url, data=data, headers=headers)
        if not res:
            res = {}
        print(f"推送至test{res.get('data')}")
        return res


AppLogin = Login()

if __name__ == '__main__':
    d_t = DataTransmit()
    # 获取 SqlServer 数据
    while True:
        data_result = d_t.get_sql_server_data()
        # 整理格式
        keys = d_t.keys.get("get_staff_info_sql")
        data = []
        for i in data_result:
            data.append({keys[inx]: v.replace("\u3000", "") if inx == 1 else v for inx, v in enumerate(i)})
        # 接口传输数据
        res = d_t.trans_to_9511(data={"p_l": json.dumps(data)}, headers={"Authorization": d_t.token})
        print("\n\n")
        time.sleep(20)
