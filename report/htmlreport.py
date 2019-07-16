# coding:utf-8
import unittest
import HTMLTestRunner
import sys
sys.path.append('/var/lib/jenkins/workspace/birduserAPItest/')
from report.send_email import main2   #该语法为Linux下python的引用法，windows下为report.sendemail
def all_case():
    #windows的路径
    case_dir = "C:\\Users\\Magic\\PycharmProjects\\elive_interface\\interface"
    #Linux的路径 可运行之后再根据workspace的路径进行调试
    #case_dir = "/var/lib/jenkins/workspace/elive_interface/interface"
    #创建unittest套件
    testcase = unittest.TestSuite()
    #查询以test开头的.py文件
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    #for test_suite in discover:
    #    for test_case in test_suite:
    #        #testunit.addTests(test_case)
    #       # print(testunit)
    print("discover",discover)
    #添加查询到的测试用例
    testcase.addTests(discover)
    print("aa",testcase)
    return testcase
#运行
if __name__ == "__main__":

    report_path="C:\\Users\\Magic\\PycharmProjects\\elive_interface\\report\\result.html"
    #report_path="/var/lib/jenkins/workspace/elive_interface/report/result.html"
    #wb 以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    fp= open(report_path,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'易直播移动端API测试报告',
                                           description=u'用例执行结果')
    #runner = unittest.TextTestRunner()
    # run所有用例
    print(u"测试用例开始执行，请耐心等待")
    runner.run(all_case())
    print(u"测试用例执行已结束")
    fp.close()
    print(u"即将发送邮件，请稍等")
    main2()
    print(u"邮件发送成功，请注意查收")