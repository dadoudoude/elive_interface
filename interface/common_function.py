import json,re,requests,urllib3,threading,time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
host = "https://dev.yizhibo.tv"
#信息头
def headers(sessionid):
    data={
        "sessionid":sessionid
    }
    return data
#礼物数据
def gift_data(num,name,vid,goodsid,sessionid):
    data={"number":num,
    "name":name,
    "vid":vid,
    "goodsid":goodsid,
    "sessionid":sessionid}
    return data
#登录
def login_data(password,phonenumber):
    data={"dev_token":"863293039381774",
        #123456hash结果为"e10adc3949ba59abbe56e057f20f883e"
        "password":password,
        "gps_latitude":30.542055,
        "token":"86_"+str(phonenumber),
        "mac":"02:00:00:00:00:00",
        "trace_id":"dc5466a8583bf32ad62ee9fdba478f98",
        "app_id":"AliPushId",
        "gps_longitude":104.060593,
        "channel_id":"a_e26d04e49349435f86aa407f939a436a",
        "authtype":"phone"
    }
    return data
#购买贵族
def buynoble(level,ecoin,rebate,continued,vid,sessionid):
    data={
       "noble_level":level,
        "ecoin":ecoin,
        "rebate_ecoin":rebate,
        "continued":continued,
        "vid":vid,
        "sessionid":sessionid
    }
    return data
#购买商城商品
def shopping(sessionid,type_num,business_id,goods_type,goods_title,goods_cost_type,goods_cost,num):
    data={
        "sessionid":sessionid,
        "type":type_num,
        "business_id":business_id,
        "goods_type":goods_type,
        "goods_title":goods_title,
        "goods_cost_type":goods_cost_type,
        "goods_cost":goods_cost,
        "goods_quantity":num
    }
    return data
#获取商城商品的各类信息
def get_goodsinfo(goodsinfo):
    mall_list=goodsinfo.content.decode("unicode_escape")
    #第一次截取
    list1=re.findall(r'"list":(.+?)}}',mall_list)
    print("get_nolble:",list1)
    #截取商品id
    goods_id=re.findall(r":(.+?),",str(re.findall(r"id(.+?)title",str(list1))))
    print("e_coupon_id:",goods_id)
    #截取商品价格
    goods_cost=re.findall(r":(.+?),",str(re.findall(r'cost"(.+?)cert_name',str(list1))))
    print("e_coupon_cost",goods_cost)
    #截取商品名称
    goods_title=re.findall(r':(.+?),',str(re.findall(r"title(.+?)description",str(list1))))
    print("e_coupon_title",goods_title)
    #截取商品类型
    goods_type=re.findall(r":(.+?),",str(re.findall(r"goods_type(.+?)cost_type",str(list1))))
    print("e_coupon_type",goods_type)
    #截取商品消费类型
    goods_cost_type=re.findall(r":(.+?),",str(re.findall(r"cost_type(.+?)cost",str(list1))))
    print("e_coupon_cost_type",goods_cost_type)
    #获取商品数量
    goods_num=re.findall(r":(.+?),",str(re.findall(r"stock(.+?)sale_count",str(list1))))
    print("e_coupon_num",goods_num)
    return goods_id,goods_cost,goods_title,goods_type,goods_cost_type,goods_num
#获取靓号的id和type
def get_number(goodsinfo):
    eightnumber_info=goodsinfo.content.decode("unicode_escape")
    list1=re.findall(r'"list":(.+?)}}',eightnumber_info)
    goods_id=re.findall(r":(.+?),",str(re.findall(r"good_number_id(.+?)name",str(list1))))
    goods_type=re.findall(r":(.+?),",str(re.findall(r'"cost_type(.+?),',str(list1))))
    return goods_id,goods_type
#购买靓号
def buy_number(sessionid,goods_type,business_id):
    data={
        "sessionid":sessionid,
        "type":goods_type,
        "business_id":business_id
    }
    return data

def get_packagegoods_info(package_info):
    package_list=package_info.content.decode("unicode_escape")
    print(package_list)
    #第一次截取
    list01=re.findall(r'"list":(.+?)}}',package_list)
    print("package_list:",list01)
    #截取道具类型
    package_type=re.findall(r":(.+?),",str(re.findall(r"type(.+?)limit_end_time",str(list01))))
    print("package_type:",package_type)
    #截取道具tool_id
    package_id=re.findall(r":(.+?),",str(re.findall(r"tool_id(.+?)tool_name",str(list01))))
    print("package_id:",package_id)
    return package_type,package_id
#提取贵族礼物等级以判断其位置和id
def get_noblegift_id(getparamnew):
    getparamnewinfo=getparamnew.content.decode("unicode_escape")
    print("a:",getparamnewinfo)
    #第一次截取
    noble_giftinfo=re.findall(r"guardian_level(.+?)gift_quantity",getparamnewinfo)
    print("b:",noble_giftinfo)
    #提取noble_type位置
    noble_type=re.findall(r'"type"(.+?)"pic"',str(noble_giftinfo))
    print("c:",noble_type)
    noble_type_position=noble_type.index(':7,')
    #提取id
    noble_id=re.findall(r'"id"(.+?)"name"',str(noble_giftinfo))[noble_type_position][1:-1]
    print("noble_id: ",noble_id)
    #提取noble第一个专属礼物对应的贵族等级
    noble_level=re.findall(r'"noble_level"(.+?)},{',str(noble_giftinfo))[noble_type_position][1:]
    return noble_id,noble_level
#主播端心跳
def perm_heart(vid,sessionid):
    requests.get(host+"/dev/appgw/liveupdatestatus?status=0&vid="+vid+"&sessionid="+sessionid,verify=False)
    time.sleep(3)
