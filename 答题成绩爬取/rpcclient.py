# -*- coding: utf-8 -*-

import pickle
import time
import selenium.common.exceptions
import pandas as pd
import openpyxl



class RPCProxy(object):
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        # 通过name，得到一个函数
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result

        return do_rpc


def get(driver):

    def logincscec():
        driver.get('https://www.cscec83.cn/user/login')
        time.sleep(1)  # 让操作稍微停一下
        # 找到输入账号的框，并自动输入账号 这里要替换为你的登录账号
        print("正在登录……")
        driver.find_element_by_id('username').send_keys('502A3297')
        time.sleep(1)
        # 密码，这里要替换为你的密码
        driver.find_element_by_id('password').send_keys('502A3297')
        time.sleep(1)

    def switchtab(num):
        handles = driver.window_handles
        driver.switch_to.window(handles[num-1])

    def exportexcel(export):
        pf = pd.DataFrame.from_dict(export, orient='index')
        file_name = '越东路答题成绩' + time.strftime("%Y-%m-%d", time.localtime()) + '.xlsx'
        file_path = pd.ExcelWriter(file_name)
        pf.to_excel(file_path, encoding='utf-8')
        file_path.save()
        print(file_name+"已保存")

    starttime = time.time()
    # 登录学习平台
    str1 = input("是否需要打开窗口并登录学习平台？ 任何输入都将视为需要登录： \n")
    if str1 != "":
        logincscec()
    str2 = input("开始读取分数？\n")
    # if str2 != "":
    #     break

    switchtab(2)
    curr = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]')
    ns = {}
    # 跳转多少页
    pages = 200
    for n in range(0, pages):
        obj = curr.find_elements_by_class_name('ranking_item')
        for i in obj:
            name = i.find_element_by_class_name('ranking_item_user_name').text
            score = i.find_element_by_class_name('ranking_item_user_text').text
            ns[name] = score
        try:
            driver.find_element_by_class_name('btn-next').click()
            # time.sleep(200)
        except selenium.common.exceptions.StaleElementReferenceException:
            print("到底了没法点")
        except:
            print("总之发生了什么错误")
    print(ns)
    ydl = {}
    ydlname = ['谈宏生', '杨剑源', '林政', '马浩斌', '李志敏', '雷永', '夏钊', '万和伟',  '王武宾', '程志强',  '李北京', '张来龙', '万林林',
               '丁维祺', '高明亮', '李洪江', '余珍顺', '董宙', '薛阳', '王熠']
    for na in ydlname:
        if na in ns:
            ydl[na] = ns[na]
        else:
            ydl[na] = '0'
            print(na, "好像没有成绩")
    # 将越东路的成绩导出excel
    exportexcel(ydl)

    endtime = time.time()
    print("本次运行耗时" + str(round(endtime - starttime, 2)) + "秒")

    # 远程连接并且调用


if __name__ == '__main__':
    from multiprocessing.connection import Client

    rpc_client = Client(('localhost', 17001), authkey=b'tab_space')
    proxy = RPCProxy(rpc_client)
    b = proxy.add()
