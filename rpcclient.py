# -*- coding: utf-8 -*-

import pickle
import time


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

    # 主程序部分自此开始：
    starttime = time.time()









    # str2 = input("开始读取分数？\n")
    # if str2 != "":
    #     break

    # switchtab(2)
    # curr = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]')
    # ns = {}
    # # 跳转多少页
    # pages = 200
    # for n in range(0, pages):
    #     obj = curr.find_elements_by_class_name('ranking_item')
    #     for i in obj:
    #         name = i.find_element_by_class_name('ranking_item_user_name').text
    #         score = i.find_element_by_class_name('ranking_item_user_text').text
    #         ns[name] = score
    #     try:
    #         driver.find_element_by_class_name('btn-next').click()
    #         # time.sleep(200)
    #     except selenium.common.exceptions.StaleElementReferenceException:
    #         print("到底了没法点")
    #     except:
    #         print("总之发生了什么错误")
    # print(ns)
    # ydl = {}
    # ydlname = ['谈宏生', '杨剑源', '林政', '马浩斌', '李志敏', '雷永', '夏钊', '万和伟',  '王武宾', '程志强',  '李北京', '张来龙', '万林林',
    #            '丁维祺', '高明亮', '李洪江', '余珍顺', '董宙', '薛阳', '王熠']
    # for na in ydlname:
    #     if na in ns:
    #         ydl[na] = ns[na]
    #     else:
    #         ydl[na] = '0'
    #         print(na, "好像没有成绩")
    # # 将越东路的成绩导出excel
    # exportexcel(ydl)

    endtime = time.time()
    print("本次运行耗时" + str(round(endtime - starttime, 2)) + "秒")

    # 远程连接并且调用


if __name__ == '__main__':
    from multiprocessing.connection import Client

    rpc_client = Client(('localhost', 17001), authkey=b'tab_space')
    proxy = RPCProxy(rpc_client)
    b = proxy.add()
