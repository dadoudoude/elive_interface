#coding:utf-8
import requests
import urllib3
import json
import time,random,xdrlib,re
import unittest
agreement="https://"
host = "dev.yizhibo.tv"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Test(unittest.TestCase):

    def setUp(self):
        print("start")
    def tearDown(self):
        time.sleep(1)
        print("the end")

    def test_register(self):
        #随机选择手机号前三位
        num2=["134","135","136","137","138","139","150","151","152","158","159","157","187","188","147","130","131","132","155","156","185","186","133","153","180","189"]
        company=random.choice(num2)
        #模拟手机号后8位
        num1=random.randint(10000000,99999999)
        #组合手机号
        phonenumber=int(company+str(num1))
        print(phonenumber)
        #发送短信
        send_short_message=requests.get(agreement+host+"/dev/appgw/smssendnew?phone=86_"+str(phonenumber)+"&sign=56dacea3fa1364853b0d8415e6e94e2e&random=0.8725844030430345&type=0&appkey=yizhibo",verify=False)
        print("send:",send_short_message.text)
        print(agreement+host+"/dev/appgw/smssendnew?phone=86_"+str(phonenumber)+"&sign=56dacea3fa1364853b0d8415e6e94e2e&random=0.8725844030430345&type=0&appkey=yizhibo")
        print(send_short_message.status_code)
        #登录后台获取手机验证码
        #登录信息
        login_data={
            "username":"admin",
            "password":"yizhibo",
            "type":0
        }
        #登录
        login=requests.post("http://dev.yizhibo.tv/user/wugangli/opadmin-e/Login/register",data=login_data,verify=False)
        cookies1="PHPSESSID="+login.cookies['PHPSESSID']
        print(login.cookies['PHPSESSID'])
        print(login.headers)
        headerInfo={
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":cookies1
        }
        #获取短信验证码
        get_short_message=requests.get("http://dev.yizhibo.tv/user/wugangli/opadmin-e/Sms/show",headers=headerInfo)
        #print(get_short_message.text)
        short_message=re.findall(r"td(.+?)td",get_short_message.text)[1][1:-2]
        print(short_message)
        #验证短信码是否正确、过期
        insuer_short_message=requests.get(agreement+host+"/dev/appgw/smsverify?authtype=phone&sms_code="+short_message+"&sms_id=5402",verify=False)
        print(agreement+host+"/appgw/smsverify?authtype=phone&sms_code="+short_message+"&sms_id=5402")
        self.assertIn("ok",insuer_short_message.text)
        #拼凑注册data
        a_z=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        gender=["male","female"]
        register_data1={
            "dev_token":"863293039381774",
            "password":"e10adc3949ba59abbe56e057f20f883e",#密码123456
            "nickname":random.choice(a_z)+random.choice(a_z)+random.choice(a_z)+str(random.randint(1-99)),
            "token":"86_"+str(phonenumber),
            "mac":"02:00:00:00:00:00",
            "trace_id":"dc5466a8583bf32ad62ee9fdba478f98",
            "phone":"86_"+str(phonenumber),
            "app_id":"AliPushId",
            "gender":random.choice(gender),
            "birthday":"1990-6-15",
            "authtype":"phone",
            "location":"中国",
            "gps_latitude":30.542055,
            "gps_longitude":104.060593,
            "channel_id":"a_e26d04e49349435f86aa407f939a436a",
            "invite_code":57777777
        }
        register_data=json.dumps(register_data1)
        #注册
        register=requests.post(agreement+host+"/dev/appgw/userregister?",data=register_data,verify=False)
        print(register.text)
        print(register.status_code)





        
