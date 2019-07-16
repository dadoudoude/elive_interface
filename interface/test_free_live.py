#encoding:utf-8
import random
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


    def test_freelive_watcher(self):
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

        #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)
        #开启直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart.text)

        #赠送礼物：么么哒*1
        send_Agift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 332, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Agift01.text)
        #获取饭团数
        get_riceroll1=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll1=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll1.text))[4:-4])
        self.assertTrue(riceroll1>riceroll0)

        #赠送幸运礼物：幸运1黑丝*1
        send_Bgift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 309, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Bgift01.text)
        #获取饭团数
        get_riceroll2=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll2=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll2.text))[4:-4])
        self.assertTrue(riceroll2>riceroll1)

        #赠送钻石礼物:10钻石礼物*1
        send_Cgift01=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, 308, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Cgift01.text)
        #获取饭团数
        get_riceroll3=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll3=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll3.text))[4:-4])
        self.assertTrue(riceroll3>riceroll2)

        #赠送普通礼物*2
        send_Agift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(2, perf_name, vid, 332, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Agift02.text)
        #获取饭团数
        get_riceroll4=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll4=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll4.text))[4:-4])
        self.assertTrue(riceroll4>riceroll3)

        #赠送幸运礼物：幸运1黑丝*520
        send_Bgift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(520, perf_name, vid, 309, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Bgift02.text)
        #获取饭团数
        get_riceroll5=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll5=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll5.text))[4:-4])
        self.assertTrue(riceroll5>riceroll4)

        #赠送钻石礼物:10钻石礼物*9
        send_Cgift02=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(9, perf_name, vid, 308, sessionid_watcher), verify=False)
        self.assertIn("ok",send_Cgift02.text)
        #获取饭团数
        get_riceroll6=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll6=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll6.text))[4:-4])
        self.assertTrue(riceroll6>riceroll5)

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
            #获取饭团数
            get_riceroll7=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
            riceroll7=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll7.text))[4:-4])
            self.assertTrue(riceroll7>riceroll6)
            print("这是第",i+1,"次")

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

        #开通贵族
        level=random.randint(0,len(noble_level)-1)
        buy_noble=requests.post(host +"/dev/appgw/buynoble?", data=common_function.buynoble(noble_level[level], noble_ecoin[level], retbate_coin[level], 0, vid, sessionid_watcher), verify=False)
        self.assertIn("ok",buy_noble.text)
        #贵族续费
        noble_continue=requests.post(host +"/dev/appgw/buynoble?", data=common_function.buynoble(noble_level[level], noble_ecoin[level], retbate_coin[level], 0, vid, sessionid_watcher), verify=False)
        self.assertIn("ok",noble_continue.text)
        #贵族自动续费
        noble_auto_continue=requests.post(host +"/dev/appgw/buynoble?", data=common_function.buynoble(noble_level[level], noble_ecoin[level], retbate_coin[level], 1, vid, sessionid_watcher), verify=False)
        self.assertIn("ok",noble_auto_continue.text)
        #获取专属礼物
        getparamnew=requests.get(host+"/dev/appgw/getparamnew?devtype=android&sessionid="+sessionid_watcher,verify=False)
        #获取第一个位置的专属礼物id和对应等级(备用)
        #noblegift= common_function.get_noblegift_id(getparamnew)
        #print("noblegift_id",noblegift,int(noblegift[1]))
        #gift_position=int(noblegift[1])-1
        #print("position",gift_position)
        #获取第一个位置的专属礼物id和对应等级
        noblegift= common_function.get_noblegift_id(getparamnew)
        print("noblegift_id",noblegift[0],int(str(noblegift[1])[:-10]))
        gift_position=noble_level.index(str(noblegift[1])[:-10])
        print("position",gift_position)
        #购买第一个贵族专属礼物对应的等级
        #开通贵族
        buy_noble=requests.post(host +"/dev/appgw/buynoble?", data=common_function.buynoble(noble_level[gift_position], noble_ecoin[gift_position], retbate_coin[gift_position], 0, vid, sessionid_watcher), verify=False)
        self.assertIn("ok",buy_noble.text)
        #赠送贵族专属礼物
        print(common_function.gift_data(1, perf_name, vid, noblegift[0], sessionid_watcher))
        noble_gift=requests.post(host +"/dev/appgw/pay/buy?", data=common_function.gift_data(1, perf_name, vid, noblegift[0], sessionid_watcher), verify=False)
        self.assertIn("ok",noble_gift.text)
        #获取饭团数
        get_riceroll8=requests.get(host+"/dev/appgw/pay/asset?sessionid="+sessionid_perf,verify=False)
        riceroll8=int(str(re.findall(r"riceroll(.+?)limitcash",get_riceroll8.text))[4:-4])
        self.assertTrue(riceroll8>riceroll7)

        ###商城###

        #获取商城电子券列表
        get_e_coupon_list=requests.get(host+"/wgl/shop/goodslist?sessionid="+sessionid_watcher+"&type=2&number_type=1&goods_type=2,5&start=0&count=6",verify=False)
        self.assertIn("ok",get_e_coupon_list.text)
        #用正则筛选各类信息
        e_coupon_info= common_function.get_goodsinfo(get_e_coupon_list)
        #商品数量
        e_coupon__num=e_coupon_info[-1]
        #购买电子券商品，2代表电子券
        #获取商品数量最多的
        max_num=str(max(map(int,e_coupon__num)))
        if int(max_num)>0:
            #判断数量最多的位置
            e_coupon__position=e_coupon__num.index(max_num)
            #购买电子券
            e_shopping=requests.post(host +"/wgl/shop/goodsbuy", data=common_function.shopping(sessionid_watcher, 2, e_coupon_info[0][e_coupon__position], e_coupon_info[3][e_coupon__position], e_coupon_info[2][e_coupon__position], e_coupon_info[4][e_coupon__position], e_coupon_info[1][e_coupon__position], 1), verify=False)
            #判断返回接口内容
            self.assertIn("ok",e_shopping.text)
            print(e_shopping.content.decode("unicode_escape"))
        else:
            print(r"商城没有可购买的电子券")

        #购买认证
        #获取认证商品列表
        get_authen_list=requests.get(host+"/wgl/shop/goodslist?sessionid="+sessionid_watcher+"&type=2&number_type=1&goods_type=3&start=0&count=6",verify=False)
        print(get_authen_list.text)
        authen_info= common_function.get_goodsinfo(get_authen_list)
        authen_num=authen_info[-1]
        print(len(authen_info),authen_info)
        #获取商品数量最多的
        max_num1=str(max(map(int,authen_num)))
        print(max_num1)
        if int(max_num1)>0:
            #最大值的位置
            authen_position=authen_num.index(max_num1)
            #购买认证
            authen_shopping=requests.post(host +"/wgl/shop/goodsbuy", data=common_function.shopping(sessionid_watcher, 2, authen_info[0][authen_position], authen_info[3][authen_position], authen_info[2][authen_position], authen_info[4][authen_position], authen_info[1][authen_position], 1), verify=False)
            #判断返回内容
            self.assertIn("ok",authen_shopping.text)
            #打印返回后的内容
            print(authen_shopping.content.decode("unicode_escape"))
        else:
            print(r"商城没有可购买的认证")

        #购买座驾
        #获取座驾靓号商品列表
        seat_list=requests.get(host+"/wgl/shop/goodslist?sessionid="+sessionid_watcher+"&type=2&number_type=2&goods_type=4&start=0&count=6",verify=False)
        print(seat_list.text)
        seat_info= common_function.get_goodsinfo(seat_list)
        seat_num=seat_info[-1]
        print(len(seat_info),seat_num)
        #获取商品数量最多的
        max_num4=str(max(map(int,seat_num)))
        print(max_num4)
        if int(max_num4)>0:
            #最大值的位置
            seat_position=seat_num.index(max_num4)
            #购买生日靓号
            seat_shopping=requests.post(host +"/wgl/shop/goodsbuy", data=common_function.shopping(sessionid_watcher, 2, authen_info[0][seat_position], authen_info[3][seat_position], authen_info[2][seat_position], authen_info[4][seat_position], authen_info[1][seat_position], 1), verify=False)
            #判断返回内容
            self.assertIn("ok",seat_shopping.text)
            #打印返回后的内容
            print(r"座驾购买：",seat_shopping.content.decode("unicode_escape"))
        else:
            print(r"商城没有可购买的座驾")

        #购买8位靓号
        #获取8位靓号的礼物信息
        get_eightnumber_list=requests.get(host+"/wgl/shop/goodslist?sessionid="+sessionid_watcher+"&type=1&number_type=1&goods_type=0&start=0&count=6",verify=False)
        self.assertIn("ok",get_eightnumber_list.text)
        #提取id和type
        eightnumber_info= common_function.get_number(get_eightnumber_list)
        #购买8位靓号
        buy_eightnumber=requests.post(host +"/wgl/shop/goodsbuy", data=common_function.buy_number(sessionid_watcher, eightnumber_info[1][0][:-1], eightnumber_info[0][0]), verify=False)
        self.assertIn("ok",buy_eightnumber.text)

        #购买生日靓号
        #获取生日靓号信息
        get_birth_list=requests.get(host+"/wgl/shop/goodslist?sessionid="+sessionid_watcher+"&type=1&number_type=2&goods_type=0&start=0&count=6",verify=False)
        print(get_birth_list.text)
        #提取id和type
        birth_info= common_function.get_number(get_birth_list)
        #购买生日靓号
        buy_eightnumber=requests.post(host +"/wgl/shop/goodsbuy", data=common_function.buy_number(sessionid_watcher, birth_info[1][0][:-1], birth_info[0][0]), verify=False)
        self.assertIn("ok",buy_eightnumber.text)

        #结束直播
        livestop=requests.get(host+"/dev/appgw/livestop?vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",livestop.text)



    def test_freelive_shopping(self):
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
        #提取观看端的易播号name
        watcher_name=str(re.findall(r"name(.+?)nickname",login_watcher.text))[5:-5]
        print("watcher_name:",watcher_name)
        #获取sessionid
        sessionid_watcher=str(re.findall(r"sessionid(.+?)auth",login_watcher.text))[5:-5]
        print("watcher sessionid:",sessionid_watcher)

        #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)
        #开启直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart.text)


        #普通单抽
        #普通十连抽


        #高级单抽
        get_high_one=requests.get(host+"/dev/agservice/admin/superlottery?vid="+vid+"&sessionid="+sessionid_watcher+"&number=1",verify=False)
        self.assertIn("ok",get_high_one.text)
        #高级十连抽
        get_high_ten=requests.get(host+"/dev/agservice/admin/superlottery?vid="+vid+"&sessionid="+sessionid_watcher+"&number=10",verify=False)
        self.assertIn("ok",get_high_ten.text)
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

        #购买/续费默默守护
        buy_momo=requests.get(host+"/dev/appgw/pay/buyguardian?vid="+vid+"&guardianid=1&to_user="+perf_name+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",buy_momo.text)
        #购买/续费一生守护
        buy_alive=requests.get(host+"/dev/appgw/pay/buyguardian?vid="+vid+"&guardianid=2&to_user="+perf_name+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",buy_alive.text)
        #购买/续费珍爱守护
        buy_love=requests.get(host+"/dev/appgw/pay/buyguardian?vid="+vid+"&guardianid=3&to_user="+perf_name+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",buy_love.text)

        #抢座
        grab_seat=requests.get(host+"/dev/appgw/grabseat?name="+perf_name+"&vid="+vid+"&sessionid="+sessionid_watcher+"&level=1&ecoin=100",verify=False)
        self.assertIn("ok",grab_seat.text)
        #弹幕
        bulletscreen=requests.get(host+"/dev/appgw/bulletscreen?content="+"asd"+"&vid="+vid+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",bulletscreen.text)


        #主播开启秘聊接单
        anchorstartsolo=requests.get(host+"/dev/appgw/anchorstartsolo?type=2&price=10&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorstartsolo.text)
        print("anchorstartsolo:",anchorstartsolo.text)
        solo_id=str(re.findall(r"solo_id(.+?)channel_id",anchorstartsolo.text))[4:-4]
        #主播端心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #客户端发起秘聊申请
        usercallsolo=requests.get(host+"/dev/appgw/usercallsolo?solo_id="+solo_id+"&sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usercallsolo.text)
        print("usercallsolo:",usercallsolo.text)
        #客户端心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #主播端结束直播
        livestop=requests.get(host+"/dev/appgw/livestop?vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",livestop.text)
        #主播端接受秘聊
        anchoracceptsolo=requests.get(host+"/dev/appgw/anchoracceptsolo?accept=1&username="+watcher_name+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchoracceptsolo.text)
        print("anchoracceptsolo:",anchoracceptsolo.text)
        #主播端心跳
        anchorsoloheartbt=requests.get(host+"/dev/appgw/anchorsoloheartbt?sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",anchorsoloheartbt.text)
        #客户端心跳
        usersoloheartbt=requests.get(host+"/dev/appgw/usersoloheartbt?sessionid="+sessionid_watcher,verify=False)
        self.assertIn("ok",usersoloheartbt.text)
        #客户端退出秘聊
        stopsolo=requests.get(host+"/dev/appgw/stopsolo?sessionid="+sessionid_watcher,verify=False)
        #self.assertIn("ok",stopsolo.text)
        print("stopsolo:",stopsolo.text)


    def test_freelive_performer(self):
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

        #观众登录
        login_watcher=requests.post(host +"/dev/appgw/userlogin?", data=common_function.login_data("e10adc3949ba59abbe56e057f20f883e", 13399778866), verify=False)
        #验证返回内容中是否有“ok”字样
        self.assertIn("ok",login_watcher.text)
        #提取观看端的易播号name
        watcher_name=str(re.findall(r"name(.+?)nickname",login_watcher.text))[5:-5]
        print("watcher_name:",watcher_name)
        #获取sessionid
        sessionid_watcher=str(re.findall(r"sessionid(.+?)auth",login_watcher.text))[5:-5]
        print("watcher sessionid:",sessionid_watcher)

        #准备直播，获取vid
        prepare=requests.get(host+"/dev/appgw/liveprepare?switch=false&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",prepare.text)
        #提取返回内容中的vid
        vid=str(re.findall(r"vid(.+?)live_url",prepare.text))[5:-5]
        print("vid:",vid)
        #开启直播
        livestart=requests.get(host+"/dev/appgw/livestart?vid="+vid+"&quality=normal&permission=0&thumb=0&sessionid="+sessionid_perf+"&title=performer%E5%B8%A6%E4%BD%A0%E8%BA%AB%E4%B8%B4%E5%85%B6%E5%A2%83%EF%BC%8C%E4%B8%8D%E5%AE%B9%E9%94%99%E8%BF%87&gps_latitude=30.542094&mode=0&gps=1&accompany=0&nettype=wifi&gps_longitude=104.061429&cp=V0_P1_S0_E1_R1_B0_A0_CN_M0",verify=False)
        self.assertIn("ok",livestart.text)

        #主播发红包
        createredpack=requests.get(host+"/dev/appgw/pay/createredpack?count=10&vid="+vid+"&sessionid="+sessionid_perf+"&title=%E6%81%AD%E5%96%9C%E5%8F%91%E8%B4%A2%EF%BC%8C%E5%A4%A7%E5%90%89%E5%A4%A7%E5%88%A9%EF%BC%81&ecoin=20",verify=False)
        self.assertIn("ok",createredpack.text)
        print(createredpack.text)
        #从系统消息中找到红包消息
        #get_redpack_info=requests.get("http://123.57.240.208:3100/getstatus?gid=0&vid="+vid+"&sid=rDg2T6VDLQMjTrUgjbHVEJlLjReNxKuk&hid=475&lt=1561357084&cid=0&aid=37&cnt=0")
        #print(get_redpack_info.text)
        #pack_code=str(re.findall(r'hb(.+?)hnm',get_redpack_info.text))
        #print("pack_code",pack_code)
        #客户端打开红包
        #redpack=requests.get(host+"/dev/appgw/pay/redpack?vid="+vid+"&code=dqssmvmg"+pack_code+"esox0040xmty10&sessionid="+sessionid_watcher,verify=False)
        #print(redpack.text)

        #主播发送弹幕
        perf_bulletscreen=requests.get(host+"/dev/appgw/bulletscreen?content="+"asd"+"&vid="+vid+"&sessionid="+sessionid_perf,verify=False)
        self.assertIn("ok",perf_bulletscreen.text)

        #抽奖单抽
        #抽奖十连抽

        #












