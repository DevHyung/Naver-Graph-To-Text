"""
title           :main.py
description     :This will convert graph (naver keyword result ) to text or csv file
author          :DevHyung
date            :2018.01.03
version         :1.0.0
usage           :python3 main.py
python_version  :3.6
required module :selenium+chromewebdriver, csv, bs4
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from CONFIG import *
import operator
import time
if __name__=="__main__":
    # Setting variable
    dir = './chromedriver'  # Driver Path
    driver = webdriver.Chrome(dir)
    # Login start
    driver.get("https://searchad.naver.com/")  # target page
    driver.find_element_by_xpath('//*[@id="uid"]').send_keys(NAVER_ID)
    driver.find_element_by_xpath('//*[@id="upw"]').send_keys(NAVER_PW)
    driver.find_element_by_xpath('//*[@id="container"]/main/div/div[1]/home-login/div/fieldset/span/button').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/my-app/wrap/welcome-beginner-layer-popup/div[2]/div[1]/a').click()
    driver.find_element_by_xpath('//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[3]/a').click()
    driver.switch_to.window(driver.window_handles[1])
    # Login end

    # if event evoke, parsing start
    input("수집 ?::")
    bs4 = BeautifulSoup(driver.page_source,"lxml")
    table = bs4.find('table',class_="layout-table")
    path = table.find('g',class_="highcharts-markers highcharts-series-0 highcharts-tracker")
    pathlist = path.find_all('path')
    print(pathlist)
    now = driver.current_window_handle
    driver.switch_to.window(now)
    #꺾은선
    """
    datadic = {}
    for test in driver.find_elements_by_tag_name('path')[34:62]:
        try:
            hover = ActionChains(driver).move_to_element(test)
            hover.perform()
            bs4 = BeautifulSoup(driver.page_source,"lxml")
            div = bs4.find('div',class_='highcharts-tooltip')
            key,data = str(div.get_text()).split(':')
            datadic[key] = data
        except:
            print("오류")
    datadic = sorted(datadic.items(), key=operator.itemgetter(0))
    print (datadic)
    """
    #왼쪽아래 막대
    idx = 0
    datadictBySex = {}
    for test in driver.find_elements_by_tag_name('rect')[:10]:
        try:
            hover = ActionChains(driver).move_to_element(test)
            hover.perform()
            bs4 = BeautifulSoup(driver.page_source, "lxml")
            div = bs4.find('div', id='highcharts-4').find('div',class_='highcharts-tooltip')
            key, data = str(div.get_text()).split(':')
            datadictBySex[key] = data
            idx+=1
            if idx > 4:
                break
        except:
            print("wait...")
    datadictByAge = {}
    idx = 0
    for test in driver.find_elements_by_tag_name('rect'):
        try:
            hover = ActionChains(driver).move_to_element(test)
            hover.perform()
            tmp = driver.find_element_by_tag_name('path')
            hovertmp = ActionChains(driver).move_to_element(tmp)
            hovertmp.perform()
            hovertmp.click()
            time.sleep(1)
            bs4 = BeautifulSoup(driver.page_source, "lxml")
            div = bs4.find('div', id='highcharts-6').find('div',class_='highcharts-tooltip')
            if '~' in div.get_text():
                key, data = str(div.get_text()).split(':')
                datadictByAge[key]=data
        except:
            print("wait...")
    datadictByAge = sorted(datadictByAge.items(), key=operator.itemgetter(0))
    datadictBySex = sorted(datadictBySex.items(), key=operator.itemgetter(0))
    print (datadictByAge)
    print( datadictBySex)