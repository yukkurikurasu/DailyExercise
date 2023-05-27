import time
import configparser
import traceback
import pytesseract
from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium
import pandas as pd


def read_options(cf):
    conf_info = configparser.ConfigParser()
    conf_info.read(cf, encoding="utf-8")
    global username, password, ocr
    try:
        username = conf_info.get("user_info", "username")
        password = conf_info.get("user_info", "password")
        ocr = conf_info.getboolean("ocr_func", "ocr")
    except configparser.NoSectionError:
        conf_info.add_section("user_info")
        conf_info.set("user_info", "username", "")
        conf_info.set("user_info", "password", "")
        conf_info.add_section("ocr_func")
        conf_info.set("ocr_func", "ocr", "False")
        ocr = False
    conf_info.write(open(cf, "w"))


def login_cscec(usn, psd, ocr_func_b=False):
    driver.get('https://www.cscec83.cn/user/login')
    # 找到输入账号的框，并自动输入账号
    driver.find_element(By.ID, 'username').send_keys(usn)
    time.sleep(0.3)
    # 密码
    driver.find_element(By.ID, 'password').send_keys(psd)
    time.sleep(0.3)
    if ocr_func_b:
        # 自动识别并填充验证码
        codepic = driver.find_element(By.XPATH, '//*[@id=\'formLogin\']/div[1]/div[3]/div[1]/div[4]/div[2]/img')
        codepic.screenshot("codepic.png")
        time.sleep(1)
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        somecode = pytesseract.image_to_string("codepic.png")
        driver.find_element(By.ID, 'inputCode').send_keys(somecode)
    countdown(1, "等待八三平台登陆……")


def process_close_popup():
    try:
        if ocr:
            countdown(3, "等待关闭弹窗……")
        else:
            input("是否已手动登陆八三平台？按回车后将尝试关闭平台登陆后的弹窗\n").strip()
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/button").click()
    except selenium.common.exceptions.NoSuchElementException:
        print("【异常】：找不到弹窗对应元素，可能已经关闭了弹窗")
    except selenium.common.exceptions.ElementNotInteractableException:
        print("【异常】：无法与弹窗对应元素互动，可能已经关闭了弹窗")


def process_goto_xueqilai():
    try:
        # print("尝试点击进入学习平台……")
        driver.find_element(By.XPATH,
                            "//*[@id=\"app\"]/section/section/main/div[2]/div/div/div/div[2]/div[3]/"
                            "div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]").click()
    except selenium.common.exceptions.NoSuchElementException:
        print("【异常】：找不到学习平台按钮对应元素，发生甚么事了")
    except selenium.common.exceptions.ElementNotInteractableException:
        print("【异常】：无法与平台按钮对应元素互动，可能已经关闭了弹窗")


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
    print("当前问题返回的结果是：", returned_answer)
    return returned_answer.iat[0, 2]


def click_path(path):
    driver.find_element(By.XPATH, path).click()


def dati(que_i):
    xpath_head = "//*[@id=\"app\"]/div/div[2]/div/div/div["
    xpath_select_mid = "]/div[1]/div[3]/div/div["
    xpath_select_end = "]/label/span[1]/span"
    mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
    # 读取题目
    # question_text = driver.find_element(By.CLASS_NAME, "issus-item-title-text").text
    question_text = driver.find_element(By.XPATH, xpath_head+str(que_i)+"]/div[1]/div[2]/div").text
    question_type = driver.find_element(By.XPATH, xpath_head+str(que_i)+"]/div[1]/div[1]/div[1]").text
    answer = search_for_answer(question_text, question_type)
    # 答案和确定的xpath
    for i in answer:
        xpath_answer = xpath_head + str(que_i) + xpath_select_mid + str(mapping[i]) + xpath_select_end
        click_path(xpath_answer)
    xpath_ok = xpath_head + str(que_i) + "]/div[2]/button[1]"
    # 点两次确定
    click_path(xpath_ok)
    time.sleep(0.3)
    click_path(xpath_ok)


# def dati_c():
#     endflag = "今日所获取积分已达到上限"
#     for i in range(1, 6):
#         dati(i)
#         time.sleep(0.5)
#     if endflag in driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div/div[3]").text:
#         print("该项今日积分已满，等待进入下一步操作……")
#         # 不做操作
    # else:
    #     # 点击再来一组，2-3-2是没答完满分的再来一组，2-4-2是打完满分的
    #     try:
    #         click_path("//*[@id=\"app\"]/div/div[2]/div/div/div[3]/button[2]")
    #         # click_path("//*[@id=\"app\"]/div/div[2]/div/div/div[4]/button[2]")
    #     except:
    #         print("在试图点击再来一组时报错")


def dati_process(url):
    while True:
        error_count = 0
        try:
            # 进入答题
            driver.get(url)
            time.sleep(1)
            endflag = "今日所获取积分已达到上限"
            for i in range(1, 6):
                if is_failed():
                    break
                dati(i)
                time.sleep(0.5)
            if endflag in driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div/div[3]").text:
                print("=========\n该项今日积分已满，等待进入下一步操作……\n=========")
                break
        except Exception as e:
            traceback.print_exc()
            print("发生错误，可能是学习平台未登陆，等待自动重试中……")
            # input("发生错误，可能是没有正确登陆学起来平台或未检测到得分情况，请确认登陆状态（回到三公司平台手动点击学起来按钮）后，按回车以重试").strip()
            driver.switch_to.window(handles[0])
            process_goto_xueqilai()
            driver.switch_to.window(handles[1])
            countdown(5, "等待学起来页面的登陆……")
            error_count += 1
            if error_count > 5:
                print("累计重试超过5次，跳过")
                break
            continue


def is_failed():
    try:
        if "闯关失败" in driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div/div[1]/div/div[3]").text:
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
        return False


def countdown(sec=5, text=""):
    for i in range(sec, -1, -1):
        print(f"\r倒计时{i}s："+text, end="")
        time.sleep(1)
    print()


def process_driver():
    driver.set_window_size(1280, 900)
    # 读写相关配置，登录平台
    global username, password, ocr
    username, password, ocr = "", "", False
    read_options("options.ini")
    login_cscec(username, password, ocr)

    # 关闭弹窗
    time.sleep(2)
    process_close_popup()

    # 点击打开学习平台
    time.sleep(1)
    process_goto_xueqilai()

    # 切换操作句柄进入第二页（即学习平台）
    global handles
    handles = driver.window_handles
    # print("所有句柄：", handles) print("当前的句柄：", driver.current_window_handle)
    if len(handles) > 1:
        driver.switch_to.window(handles[1])
    else:
        print("你这只有一个窗口诶")
    # 等待学起来页面的登陆，延迟5秒
    countdown(5, "等待学起来页面的登陆……")

    # 进入每日练习
    dati_process("http://120.27.194.253/org/MSXAav/paper/practice/start?practiceType=1")
    # 进入每日闯关
    dati_process("http://120.27.194.253/org/MSXAav/paper/practice/start?practiceType=2")
    driver.quit()


if __name__ == '__main__':

    starttime = time.time()
    # print("自动答题程序 v1.0.3 \nLast update: 2023/04/25")
    print("自动答题程序 v1.0.4 \nLast update: 2023/05/07")

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('-enable-webgl --no-sandbox --disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    try:
        driver = WebDriver(options=options)
        process_driver()
    except selenium.common.exceptions.SessionNotCreatedException:
        print("错误：无法启动chrome，可能是没有最新的chromedriver文件，请下载符合当前版本的chromedriver并放置在文件夹内")
        print("chromedriver下载地址：https://chromedriver.chromium.org/downloads")

    endtime = time.time()
    print("本次运行耗时" + str(round(endtime - starttime, 2)) + "秒")
    input("运行完毕，按回车以退出\n")
# D:\PythonProjects\DailyExercise\venv\Scripts\pyinstaller -F -i ico.png dati_semiauto.py
