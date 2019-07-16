#encoding:utf-8
import re
import time
import unittest

import requests
import urllib3

from interface import common_function

host = "https://dev.yizhibo.tv"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Test(unittest.TestCase):

    def setUp(self):
        print("start")
    def tearDown(self):
        time.sleep(1)
        print("the end")


    def test_watcher(self):
        #登录
        login_perf=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13340962953), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_perf.text)
        #提取主播的易播号name
        perf_name=str(re.findall(r"name(.+?)nickname",login_perf.text))[5:-5]
        print("perf_name:",perf_name)
        #获取sessionid
        sessionid_perf=str(re.findall(r"sessionid(.+?)auth",login_perf.text))[5:-5]
        print("performer sessionid:",sessionid_perf)
        #获取主播饭团数
        get_riceroll0=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",get_riceroll0.text)
        riceroll0=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll0.text))[4:-4])
        print("riceroll0",riceroll0)

        #观众登录
        login_watcher=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 18639658074), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_watcher.text)
        #获取sessionid
        sessionid_watcher=str(re.findall(r"sessionid(.+?)auth",login_watcher.text))[5:-5]
        print("watcher sessionid:",sessionid_watcher)

        #新分类列表
        topiclistnew=requests.get(host+"/dev/appgw/topiclistnew?count=10000&start=0&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",topiclistnew.text)
        #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)

        #获取用户财产信息
        asset1=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",asset1.text)
        #获取管理员列表
        usermanagerlist=requests.get(host+"/dev/appgw/usermanagerlist?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",usermanagerlist.text)
        #获取用户财产信息
        asset2=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",asset2.text)
        #获取游戏列表
        getgamelist=requests.get(host+"/dev/appgw/getgamelist?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",getgamelist.text)
        #用户基本信息
        userbaseinfo=requests.get(host+"/dev/appgw/userbaseinfo?name="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",userbaseinfo.text)
        #获取用户财产信息
        asset3=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",asset3.text)
        #获取用户背包道具
        userpackagetools=requests.get(host+"/dev/appgw/userpackagetools?&start=0&count=100000&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",userpackagetools.text)
        #获取贵族信息
        noble_data={
            "sessionid":sessionid_perf
        }
        getnobleinfo=requests.post(host+"/dev/appgw/getnobleinfo?",data=noble_data,verify=False)
        self.assertIn("ok",getnobleinfo.text)
        #获取直播间任务
        taskinlive=requests.get(host+"/dev/appgw/taskinlive?&anchor_uid="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",taskinlive.text)

        #开启直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart.text)
        #直播心跳
        getstatus0=requests.get("http://123.57.240.208:3100/getstatus?gid=-1&vid="+vid+"&sid="+sessionid_perf+"&hid=-1&lt=0&cid=0&aid=0&cnt=0")
        self.assertIn("ok",getstatus0.text)
        #上传可视云
        #clientcounter=requests.get("http://videodev.ksyun.com/univ/clientcounter?accesskey=D8uDWZ88ZKW48/eZHmRm&expire="+str(int(time.time()))+"&cont=eyJzZGtfdHlwZSI6InN0cmVhbWVyIiwic2RrX3ZlciI6IjUuMC4xLjMiLCJwbGF0Zm9ybSI6ImFuZHJvaWQiLCJvc192ZXIiOiI2LjAiLCJwa2ciOiJjb20uY2N2aWRlbyIsImRldl9tb2RlbCI6IkhVQVdFSSBWTlMtQUwwMCIsImRldl9pZCI6Ijg2MzI5MzAzOTM4MTc3NCIsImxvZ192ZXIiOiIyLjAuMSIsImxvZ192biI6MTAyfQ%3D%3D&uniqname=ksystreamer_android&signature=NhNJ7G1wz8IcJ26aOzZ2sMGzy9o%3D")
        #self.assertIn("success",clientcounter.text)
        #获取本地dns
        getlocaldns=requests.get("http://trace-ldns.ksyun.com/getlocaldns")
        self.assertIn("ClientIP",getlocaldns.text)
        print("getlocaldns:",getlocaldns.text)
        #获取

        #主播发红包
        creatredpack=requests.get(host+"/dev/appgw/pay/createredpack?count=20&vid="+vid+"&sessionid="+sessionid_perf+"&title=%E6%81%AD%E5%96%9C%E5%8F%91%E8%B4%A2%EF%BC%8C%E5%A4%A7%E5%90%89%E5%A4%A7%E5%88%A9%EF%BC%81&ecoin=50",verify=False)
        print("creatredpack:",creatredpack.text)
        #获取红包信息
        for i in range(0,3):
            getredpackinfo=requests.get("http://123.57.240.208:3100/getstatus?gid=0&vid="+vid+"&sid="+sessionid_perf+"&hid=1&lt="+str(int(time.time()))+"&cid=0&aid=0&cnt=0")
            print(i,"getredpackinfo:",getredpackinfo.text)
