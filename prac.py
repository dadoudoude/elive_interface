#encoding:utf-8
import json
import re
import time
import unittest,requests,random
import urllib3

from interface import common_function
headers={
    "Cookie":"	PHPSESSID=8c94bda02a92e551deb9222dda14621f"
}
for i in range(1,2):
    name=random.randint(10000000,99999999)
    goods_data={
        "id":"",
        "name":name,
        "cost_type":1,
        "cost":random.randint(1,100),
        "type":7,
        "status":1
    }
    #goods_data1=json.dumps(goods_data)
    add_eightnumber=requests.post("https://dev.yizhibo.tv/user/wugangli/opadmin-e/Advance_module/good_number_input",header=headers,data=goods_data,verify=False)
    print(add_eightnumber.text)