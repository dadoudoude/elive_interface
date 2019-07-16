#encoding:utf-8
import re
import time
import unittest

import requests
import urllib3

from interface import common_function

host = "https://dev.yizhibo.tv"
host1 = "http://123.57.240.208:3100"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Test(unittest.TestCase):

    def setUp(self):
        print("start")
    def tearDown(self):
        time.sleep(1)
        print("the end")


    def test_privateletter(self):
        #登录
        login_perf=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13399887766), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_perf.text)
        #提取主播的易播号name
        perf_name=str(re.findall(r"name(.+?)nickname",login_perf.text))[5:-5]
        print("perf_name:",perf_name)
        #获取sessionid
        sessionid_perf=str(re.findall(r"sessionid(.+?)auth",login_perf.text))[5:-5]
        print("performer sessionid:",sessionid_perf)
        #获取用户信息
        perf_userinfo=requests.get(host+"/dev/appgw/userinfo?name="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        print("perf_userinfo:",perf_userinfo.text)
        #提取主播私信im账号
        perf_im=str(re.findall(r'"new_imuser":(.+?),"usercenterbg"',perf_userinfo.text))[3:-3]
        print("perf_im:",perf_im)

        #观众登录
        login_watcher=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13399778866), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_watcher.text)
        #获取sessionid
        sessionid_watcher=str(re.findall(r"sessionid(.+?)auth",login_watcher.text))[5:-5]
        print("watcher sessionid:",sessionid_watcher)
        #提取主播的易播号name
        watcher_name=str(re.findall(r"name(.+?)nickname",login_watcher.text))[5:-5]
        print("watcher_name:",watcher_name)
        #获取用户信息
        watcher_userinfo=requests.get(host+"/dev/appgw/userinfo?name="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        print("watcher_userinfo:",watcher_userinfo.text)
        #提取观众私信im账号
        watcher_im=str(re.findall(r'"new_imuser":(.+?),"usercenterbg"',watcher_userinfo.text))[3:-3]
        print("watcher_im:",watcher_im)

        #私信红包
        redpack_data={
            "messageContent":[{"content":"czfeyevz1563184982pdwu0040famw10","hasTake":0,"price":20,"title":"恭喜发财，大吉大利！","type":1}],
            "messageContentType":2,
            "messageType":2,
            "receiver":perf_im,
            "sender":watcher_im,
            "sessionid":sessionid_watcher,
            "signature":"dc604b75cd80a8da3df776a51769846983092fcd"
        }
        privateredpack=requests.post(host+"/imserver/v1/message/sendmessage?",data=redpack_data,verify=False)
        print(privateredpack.text)
        creatredpack=requests.get(host+"/dev/appgw//pay/redpack/group/create?count=1&sessionid="+sessionid_watcher+"&title=%E6%81%AD%E5%96%9C%E5%8F%91%E8%B4%A2%EF%BC%8C%E5%A4%A7%E5%90%89%E5%A4%A7%E5%88%A9%EF%BC%81&ecoin=20",verify=False)
        self.assertIn("ok",creatredpack.text)

        #私信转账
        imservertransferaccounts=requests.get(host+"/dev/appgw/imservertransferaccounts?&to_name="+perf_name+"&to_imuser="+perf_im+"&ecoin=2&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",imservertransferaccounts.text)
