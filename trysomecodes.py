import time

import pandas as pd


def search_for_answer(question_text, question_type="单选题"):
    file = "试题.csv"
    csvPD = pd.read_csv(file)
    # 进行一轮筛选，确定较优的待查关键字
    if '《' in question_text:
        keyword_to_search1 = question_text[15:]
    elif "规定" in question_text:
        start = question_text.find("规定")
        keyword_to_search1 = question_text[start:start + 15]
    elif "要求" in question_text:
        start = question_text.find("要求")
        keyword_to_search1 = question_text[start:start + 15]
    else:
        keyword_to_search1 = question_text[0:10]
    returned_answer = csvPD[csvPD["question"].str.contains(keyword_to_search1)]
    # 如果含有不定空格导致查找返回空值：
    if returned_answer.empty:
        start = question_text.find(" ")
        keyword_to_search1 = question_text[start - 10:start]
        returned_answer = csvPD[csvPD["question"].str.contains(keyword_to_search1)]
    if returned_answer.empty:
        start = question_text.find(" ")
        keyword_to_search1 = question_text[start:start + 10]
        returned_answer = csvPD[csvPD["question"].str.contains(keyword_to_search1)]
    returned_answer = returned_answer[returned_answer["type"] == question_type]
    print("返回的结果是：", returned_answer)
    return returned_answer.iat[0, 0], returned_answer.iat[0, 2]


# question_text = "根据《A类基础设施业务管理手册》相关规定，以下属于A类基础设施项目的是（ ）"
# search_for_answer(question_text, question_type="多选题")
for i in range(5, -1, -1):
    print(f"\r等待学起来页面的登陆，倒计时{i}s\n", end="")
    time.sleep(1)


# import time
# from multiprocessing import Process
# import os
#
#
# # 子进程要执行的代码
# def run_proc(name):
#     for i in range(5, -1, -1):
#         print(f"\r系统倒计时{i}s", end="")
#         time.sleep(1)
#
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Process(target=run_proc, args=('test',))
#     print('Child process will start.')
#     p.start()
#     p.join()
#     print("something else")


# for i in range(5, -1, -1):
#     print(f"\r系统倒计时{i}s", end="")
#     time.sleep(1)
