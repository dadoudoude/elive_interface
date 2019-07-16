#encoding:utf-8
import json
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

        #获取直播名称
        topiclistnew=requests.get(host+"/dev/appgw/topiclistnew?count=10000&start=0&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",topiclistnew.text)
        #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)

        #准备直播
        liveprepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",liveprepare.text)
        #
        monitor1_data={"header":{"sdk_type":"streamer","sdk_ver":"5.0.1.3","platform":"android","os_ver":"6.0","pkg":"com.ccvideo","dev_model":"HUAWEI VNS-AL00","dev_id":"863293039381774","log_ver":"2.0.1","log_vn":102},"body":[{"_id":"2b89eda9-4fa4-4b64-8772-9060c40a9143","type":100,"body_type":"endStreaming","action_id":"AAC54B080AEAE89EDCBABBF9CA011A57","streamId":"AAC54B080AEAE89EDCBABBF9CA011A57","streaming_len":0,"send_slow_cnt":0,"drop_frame_cnt":0,"drop_frame_cnt_am":0,"drop_frame_cnt_bm":0,"net_type":"WIFI","net_des":"N\/A","upload_size":0,"encode_frame_cnt":0,"end_type":0,"end_role":"PUB","date":0,"audio_channels":1,"auto_adjust_bitrate":"true","is_landspace":"false","is_front_mirror":"true","iframe_interval":3,"max_video_bitrate":1200,"min_video_bitrate":500,"video_bitrate":800,"sample_audio_rate":44100,"audio_bitrate":48,"resolution":"544x864","framerate":15,"video_encode_type":"soft264","audio_encode_type":"soft_aac_he","video_encode_perf":"LowPower","live_scence":"Showself"},{"type":100,"body_type":"function_point","function_type":"display_glsurface","net_type":"WIFI","date":int(float(time.time())*1000)},{"type":100,"body_type":"beautify","beautify_type":"ImgBeautyProFilter","net_type":"WIFI","date":int(float(time.time())*1000)},{"type":100,"body_type":"beautify","beautify_type":"ImgBeautyProFilter","net_type":"WIFI","date":int(float(time.time())*1000)},{"type":100,"body_type":"beautify","beautify_type":"ImgSTFilter","net_type":"WIFI","date":int(float(time.time())*1000)}]}
        monitor1data=json.dumps(monitor1_data)
        monitor1=requests.post("http://videodev.ksyun.com:8980/univ/monitorclient?accesskey=D8uDWZ88ZKUCPu0KRJkR&expire=1562896222&uniqname=ksystreamer_android&contmd5=482ABC428C6F01E507F8F9BD501167BE&signature=35K5TgmBDGCxw5lweEYLiYI7cGU%3D",data=monitor1data,verify=False)
        print("monitor1:",monitor1.text)
        #开启付费直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=7&thumb=0&price=20&sessionid="+sessionid_perf+"&title=%E9%A1%BE%E5%AE%A2%E4%BB%AC%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542021&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.060578&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        print("livestart:",livestart.text)
        self.assertIn("ok",livestart.text)
       #
        permission=requests.get("http://dev.yizhibo.tv:8095/ieasy/pk/permission?&vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        print("permission:",permission.text)
        #付费直播ing
        #设置视频分类

        videosettopic=requests.get(host+"/dev/appgw/videosettopic?topic_id=220&vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",videosettopic.text)
        #获取房间设置信息
        getroominfo=requests.get(host+"/dev/appgw/getroominfo?vid="+vid+"&roomid="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",getroominfo.text)
        #推流？
        permission=requests.get("http://dev.yizhibo.tv:8095/ieasy/pk/permission?&vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",permission.text)
        #更新直播状态
        liveupdatestatus=requests.get(host+"/dev/appgw/liveupdatestatus?status=0&vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",liveupdatestatus.text)
        #获取用户财产信息
        getusermoney=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",getusermoney.text)
        #观众观看直播返回E_PAYMENT
        watchstart=requests.get(host+"/dev/appgw/watchstart?gps_longitude=104.060626&vid=vOxMhVkMrdFdAd&sessionid="+sessionid_watcher+"&gps_latitude=30.542037",verify=False)
        #self.assertIn("E_PAYMENT",watchstart.text)
        #观众需要付费才能观看
        watchprepare=requests.get(host+"/dev/appgw/watchprepare?gps_longitude=104.060626&gps_latitude=30.542037&vid="+vid+"&sessionid="+sessionid_watcher,verify=False)
        #self.assertIn("ok",watchprepare.text)
        #观众支付易币进入直播间
        livepay=requests.get(host+"/dev/appgw/livepay?gps_longitude=104.060626&gps_latitude=30.542037&vid="+vid+"&sessionid="+sessionid_watcher,verify=False)
        print(host+"/dev/appgw/livepay?gps_longitude=104.060626&gps_latitude=30.542037&vid="+vid+"&sessionid="+sessionid_watcher)
        print(livepay.text)


    def test_freeliv_pk(self):

        #登录PK所需账号主播1、主播2、观众
        #登录主播1
        login_perf1=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13340962953), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_perf1.text)
        #提取主播的易播号name
        perf_name1=str(re.findall(r"name(.+?)nickname",login_perf1.text))[5:-5]
        print("perf_name1:",perf_name1)
        #获取sessionid1
        sessionid_perf1=str(re.findall(r"sessionid(.+?)auth",login_perf1.text))[5:-5]
        print("performer sessionid1:",sessionid_perf1)
        #登录主播2
        login_perf2=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13340962953), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_perf2.text)
        #提取主播的易播号name
        perf_name2=str(re.findall(r"name(.+?)nickname",login_perf2.text))[5:-5]
        print("perf_name2:",perf_name2)
        #获取sessionid2
        sessionid_perf2=str(re.findall(r"sessionid(.+?)auth",login_perf2.text))[5:-5]
        print("performer sessionid2:",sessionid_perf2)

        #观众登录
        login_watcher=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 18639658074), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_watcher.text)
        #提取观看端的易播号name
        watcher_name=str(re.findall(r"name(.+?)nickname",login_watcher.text))[5:-5]
        print("watcher_name:",watcher_name)
        #获取sessionid
        sessionid_watcher=str(re.findall(r"sessionid(.+?)auth",login_watcher.text))[5:-5]
        print("watcher sessionid:",sessionid_watcher)

        #主播1准备直播，获取vid
        preparelive1=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf1,verify=False)
        self.assertIn("ok",preparelive1.text)
        #提取返回内容中的vid
        vid1=str(re.findall(r"vid(.+?)live_url",preparelive1.text))[5:-5]
        print("vid1:",vid1)
        #开启直播
        livestart1=requests.get(host+"/dev/appgw/livestart?vid="+vid1+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf1+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart1.text)
        #主播2准备直播，获取vid
        preparelive2=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf2,verify=False)
        self.assertIn("ok",preparelive2.text)
        #提取返回内容中的vid
        vid2=str(re.findall(r"vid(.+?)live_url",preparelive2.text))[5:-5]
        print("vid2:",vid2)
        #开启直播
        livestart2=requests.get(host+"/dev/appgw/livestart?vid="+vid2+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf1+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart2.text)

        #主播1开启PK
        preparepk1=requests.get("http://dev.yizhibo.tv:8095/ieasy/pk/apply?&vid="+vid1+"&sessionid="+sessionid_perf1,verify=False)
        self.assertIn("ok",preparepk1.text)
        #主播2开启PK
        preparepk2=requests.get("http://dev.yizhibo.tv:8095/ieasy/pk/apply?&vid="+vid2+"&sessionid="+sessionid_perf2,verify=False)
        self.assertIn("ok",preparepk2.text)

        #准备接受PK邀请
        acceptpk=requests.get(host+"http://dev.yizhibo.tv:8095/ieasy/pk/accept?&sessionid="+sessionid_perf1,verify=False)
        self.assertIn("ok",acceptpk.text)

        usersimpleinfo=requests.get(host+"/dev/appgw/usersimpleinfo?&name="+perf_name2+"&sessionid="+sessionid_perf1,verify=False)
        self.assertIn("ok",usersimpleinfo.text)
        enterPkSuccess=requests.get("http://dev.yizhibo.tv:8095/ieasy/pk/enterPkSuccess?&pkId=1180&sessionid=OecA3t97EMALhzyBLVMMCLL78pQj40ZS")






