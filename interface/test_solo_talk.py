#encoding:utf-8
import random
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


    def test_solotalk(self):
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
        #获取主播饭团数
        get_riceroll0=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",get_riceroll0.text)
        riceroll0=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll0.text))[4:-4])
        print("riceroll0",riceroll0)

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

        ###开启公开直播，购买贵族###
         #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)
        #开启直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart.text)
        #获取贵族信息
        get_noble=requests.post(host +"/dev/appgw/getnobleinfo?", data=common_function.headers(sessionid_watcher), verify=False)
        noble1=re.findall(r'"noble_list":(.+?)}}',get_noble.text)
        print("get_nolble:",noble1)
        #截取noble_level
        noble_level=re.findall(r":(.+?),",str(re.findall(r"noble_level(.+?)name",str(noble1))))
        print("noble_level:",noble_level)
        #截取开通贵族价值易币
        noble_ecoin=re.findall(r":(.+?),",str(re.findall(r"ecoin(.+?)rebate_ecoin",str(noble1))))
        print("noble_ecoin: ",noble_ecoin)
        #截取返回易币
        retbate_coin=re.findall(r":(.+?),",str(re.findall(r"rebate_ecoin(.+?)image_id",str(noble1))))
        print("retbate_coin:",retbate_coin)
        #开通贵族公爵或者亲王
        level=random.randint(len(noble_level)-3,len(noble_level)-2)
        buy_noble=requests.post(host +"/dev/appgw/buynoble?", data=common_function.buynoble(noble_level[level], noble_ecoin[level], retbate_coin[level], 0, vid, sessionid_watcher), verify=False)
        self.assertIn("ok",buy_noble.text)
        #获取专属礼物
        getparamnew=requests.get(host+"/dev/appgw/getparamnew?devtype=android&sessionid="+sessionid_watcher,verify=False)
        #获取第一个位置的专属礼物id和对应等级
        noblegift= common_function.get_noblegift_id(getparamnew)
        print("noblegift_id&level",noblegift[0],int(str(noblegift[1])[:-10]))
        gift_position=noble_level.index(str(noblegift[1])[:-10])
        print("position",gift_position)
        #购买珍爱守护
        buy_love=requests.get(host+"/dev/appgw/pay/buyguardian?vid="+vid+"&guardianid=3&to_user="+perf_name+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",buy_love.text)



        #主播端准备秘聊
        anchorstartsolo=requests.get(host+"/dev/appgw/anchorstartsolo?price=10&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorstartsolo.text)
        print("anchorstartsolo: ",anchorstartsolo.text)
        solo_id=re.findall(r'"solo_id":(.+?),"channel_id"',anchorstartsolo.text)
        print("solo_id: ",solo_id)
        #更新秘聊心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #观众端更新/监听秘聊请求并判断目标主播发起的秘聊是否存在
        while True:
            anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
            self.assertIn("ok",anchorsoloheartbt.text)
            sololist=requests.get(host+"/dev/appgw/sololist?&type=1&start=0&count=20&sessionid="+sessionid_watcher,verify=False)
            solonames=re.findall(r'"name":"(.+?)","location"',sololist.text)
            print(solonames)
            self.assertIn("ok",sololist.text)
            anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
            self.assertIn("ok",anchorsoloheartbt.text)
            if perf_name in solonames:
                break
        #用户向主播发起秘聊申请
        usercallsolo=requests.get(host+"/dev/appgw/usercallsolo?solo_id="+str(solo_id)[2:-2]+"&sessionid="+sessionid_watcher,verify=False)
        print("usercallsolo:",host+"/dev/appgw/usercallsolo?solo_id="+str(solo_id)[2:-2]+"&sessionid="+sessionid_watcher)
        self.assertIn("ok",usercallsolo.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #主播接受秘聊申请
        anchoracceptsolo=requests.get(host+"/dev/appgw/anchoracceptsolo?accept=1&username="+watcher_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchoracceptsolo.text)
        print("anchoracceptsolo:",anchoracceptsolo.text)
        #获取秘聊视频的VID
        vid=str(re.findall(r'"vid":(.+?),"permission"',anchoracceptsolo.text))[3:-3]
        print("vid:",vid)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #获取接受秘聊后饭团是否增加
        get_riceroll01=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll01=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll01.text))[4:-4])
        #self.assertTrue(riceroll01>riceroll0)

        #获取主播信息
        userbaseinfo=requests.get(host+"/dev/appgw/userbaseinfo?name="+perf_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",userbaseinfo.text)
        #获取主播饭团数
        asset=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        print("asset:",asset.text)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #真心话
        soloquestion1=requests.get(host+"/dev/appgw/soloquestionbuy?&questionid=1&anchorname="+perf_name+"&vid="+vid+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",soloquestion1.text)
        #判断真心话是否增加饭团
        get_riceroll02=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll02=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll02.text))[4:-4])
        self.assertTrue(riceroll02>riceroll01)
        #大冒险
        soloquestion2=requests.get(host+"/dev/appgw/soloquestionbuy?&questionid=3&anchorname="+perf_name+"&vid="+vid+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",soloquestion1.text)
        #判断大冒险是否增加饭团
        get_riceroll03=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll03=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll03.text))[4:-4])
        self.assertTrue(riceroll03>riceroll02)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #赠送礼物：么么哒*1
        send_Agift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 332, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Agift01.text)
        #获取饭团数
        get_riceroll1=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll1=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll1.text))[4:-4])
        self.assertTrue(riceroll1>riceroll03)

        #赠送幸运礼物：幸运1黑丝*1
        send_Bgift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 309, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Bgift01.text)
        #获取饭团数
        get_riceroll2=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll2=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll2.text))[4:-4])
        self.assertTrue(riceroll2>riceroll1)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #赠送钻石礼物:10钻石礼物*1
        send_Cgift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 308, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Cgift01.text)
        #获取饭团数
        get_riceroll3=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll3=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll3.text))[4:-4])
        self.assertTrue(riceroll3>riceroll2)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #赠送普通礼物*2
        send_Agift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(2, perf_name, vid, 332, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Agift02.text)
        #获取饭团数
        get_riceroll4=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll4=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll4.text))[4:-4])
        self.assertTrue(riceroll4>riceroll3)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #赠送幸运礼物：幸运1黑丝*520
        send_Bgift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(520, perf_name, vid, 309, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Bgift02.text)
        #获取饭团数
        get_riceroll5=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll5=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll5.text))[4:-4])
        self.assertTrue(riceroll5>riceroll4)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #赠送钻石礼物:10钻石礼物*9
        send_Cgift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(9, perf_name, vid, 308, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Cgift02.text)
        #获取饭团数
        get_riceroll6=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll6=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll6.text))[4:-4])
        self.assertTrue(riceroll6>riceroll5)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #随机赠送任意数量、任一礼物*3次
        for i in range(0,2):
            gifts=["308","309","332","307","311","334"]
            gift_data={
                "number":random.randint(1,20),
                "name":perf_name,
                "vid":vid,
                "goodsid":int(random.choice(gifts)),
                "sessionid":sessionid_watcher
            }
            send_gift=requests.post(host+"/dev/appgw/pay/buy?",data=gift_data,verify=False)
            self.assertIn("ok",send_gift.text)
            #维持主播心跳
            anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
            self.assertIn("ok",anchorsoloheartbt.text)
            #用户心跳
            usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
            self.assertIn("ok",usersoloheartbt.text)
            #获取饭团数
            get_riceroll7=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
            riceroll7=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll7.text))[4:-4])
            self.assertTrue(riceroll7>riceroll6)
            print("这是第",i+1,"次")
        #普通单抽
        #普通十连抽


        #高级单抽
        get_high_one=requests.get(host+"/dev/agservice/admin/superlottery?vid="+vid+"&sessionid="+sessionid_watcher+"&number=1",verify=False)
        self.assertIn("ok",get_high_one.text)
        #高级十连抽
        get_high_ten=requests.get(host+"/dev/agservice/admin/superlottery?vid="+vid+"&sessionid="+sessionid_watcher+"&number=10",verify=False)
        self.assertIn("ok",get_high_ten.text)
        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #高级百连抽
        get_high_ten=requests.get(host+"/dev/agservice/admin/superlottery?vid="+vid+"&sessionid="+sessionid_watcher+"&number=100",verify=False)
        self.assertIn("ok",get_high_ten.text)
        #送背包礼物（考虑观影券问题）
        #获取背包礼物信息
        get_package_info=requests.get(host+"/dev/appgw/userpackagetools?&start=0&count=100000&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",get_package_info.text)
        #获取礼物名称
        package_list=get_package_info.content.decode("unicode_escape")
        print(package_list)
        #获取背包道具的type和tool_id
        packagegoods_info= common_function.get_packagegoods_info(get_package_info)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #判断是否存在可赠送礼物type为1
        if '1' in packagegoods_info[0]:
            print("背包存在可赠送礼物")
            bag_position=packagegoods_info[0].index('1')
            print("bag_position",bag_position)
            tool_id=packagegoods_info[1][bag_position]
            #赠送背包道具
            send_pag_gift=requests.get(host+"/dev/appgw/usepackagetool?&number=1&touser="+perf_name+"&vid="+vid+"&usetype=1&toolid="+tool_id+"&sessionid="+sessionid_watcher,verify=False)
            print(send_pag_gift.content.decode("unicode_escape"))
            self.assertIn("ok",send_pag_gift.text)
            #获取饭团数
            get_riceroll1=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
            riceroll1=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll1.text))[4:-4])
            self.assertTrue(riceroll1>riceroll0)
        else:
            print("背包没有可赠送礼物")

        #转赠礼物
        gift_giving=requests.get(host+"/dev/appgw/usepackagetool?&toolid="+packagegoods_info[1][0]+"&usetype=2&vid="+vid+"&number=1&touser="+perf_name+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",gift_giving.text)

        #维持主播心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #用户心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)

        #赠送低等级贵族专属礼物（伯爵 342）
        noble_gift0=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 342, sessionid_watcher), verify=False)
        self.assertIn("ok",noble_gift0.text)
        #赠送高等级贵族专属礼物（皇帝 341）
        noble_gift1=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 341, sessionid_watcher), verify=False)
        self.assertIn("E_USER_NOBLE_LEVEL_LIMIT",noble_gift1.text)
        #赠送珍爱守护礼物(珍爱1 360)
        noble_gift2=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 360, sessionid_watcher), verify=False)
        self.assertIn("ok",noble_gift2.text)
        #赠送珍爱守护礼物(一生20 359)
        noble_gift3=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 359, sessionid_watcher), verify=False)
        self.assertIn("E_USER_GUARDIAN_LEVEL_LIMIT",noble_gift3.text)

