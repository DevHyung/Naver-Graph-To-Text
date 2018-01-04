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
    title = ""
    # if event evoke, parsing start
    print("Made By HONG copyright Same:")
    print("수집하려는 키워드의 PC,MOBILE 사용자 수를 입력하세요")
    numstr = input(" ex: 100,100 왼쪽과 같이 포맷을 맞춘후 입력후엔터를 누르세요 ::")
    pc,mobile = numstr.split(',')
    input("그후 키워드를 클릭후 그래프화면이 로딩되면 엔터를 누르세요 ::")

    bs4 = BeautifulSoup(driver.page_source,"lxml")
    table = bs4.find('table',class_="layout-table")
    path = table.find('g',class_="highcharts-markers highcharts-series-0 highcharts-tracker")
    pathlist = path.find_all('path')

    title = bs4.find('h4',class_='modal-title').find('span',class_='ng-binding').get_text()
    #print(pathlist)
    now = driver.current_window_handle
    driver.switch_to.window(now)
    #꺾은선
    print(">>> 꺾은선 추출 시작")
    datadic = dict([('2017-01desktop', '0'), ('2017-01mobile', '0'), ('2017-02desktop', '0'), ('2017-02mobile', '0'), ('2017-03desktop', '0'), ('2017-03mobile', '0'), ('2017-04desktop', '0'), ('2017-04mobile', '0'), ('2017-05desktop', '0'), ('2017-05mobile', '0'), ('2017-06desktop', '0'), ('2017-06mobile', '0'), ('2017-07desktop', '0'), ('2017-07mobile', '0'), ('2017-08desktop', '0'), ('2017-08mobile', '0'), ('2017-09desktop', '0'), ('2017-09mobile', '0'), ('2017-10desktop', '0'), ('2017-10mobile', '0'), ('2017-11desktop', '0'), ('2017-11mobile', '0'), ('2017-12desktop', '0'), ('2017-12mobile', '0')])
    for test in driver.find_elements_by_tag_name('path')[34:62]:
        try:
            tmp = driver.find_element_by_tag_name('path')
            hovertmp = ActionChains(driver).move_to_element(tmp)
            hovertmp.perform()
            hovertmp.click()
            hover = ActionChains(driver).move_to_element(test)
            hover.perform()
            bs4 = BeautifulSoup(driver.page_source,"lxml")
            div = bs4.find('div',class_='highcharts-tooltip')
            key,data = str(div.get_text()).split(':')
            datadic[key] = data
        except:
            print("오류")
    #datadic = sorted(datadic.items(), key=operator.itemgetter(0))
    for tmp in datadic.keys():
        if datadic[tmp] == '0':
            print(tmp, " parsing error ", end='')
            datadic[tmp] = input("input ::")
    #if len(datadic) != 24:
     #   print("::: 그래프 겹침 발견 데이터확인필요 아래에서 누락 점검")
      #  print(datadic)
    print(">>> 꺾은선 추출 종료")
    #왼쪽아래 막대
    print(">>> 왼쪽아래 추출 시작")
    idx = 0
    datadictBySex = {'남성desktop': '0', '남성mobile': '0', '여성desktop': '0', '여성mobile': '0'}
    try:
        for test in driver.find_elements_by_tag_name('rect')[:10]:
            try:
                tmp = driver.find_element_by_tag_name('path')
                hovertmp = ActionChains(driver).move_to_element(tmp)
                hovertmp.perform()
                hovertmp.click()
                hover = ActionChains(driver).move_to_element(test)
                hover.perform()
                time.sleep(0.5)
                bs4 = BeautifulSoup(driver.page_source, "lxml")
                div = bs4.find('div', id='highcharts-4').find('div',class_='highcharts-tooltip')
                key, data = str(div.get_text()).split(':')
                datadictBySex[key] = data
                idx+=1
                if idx > 4:
                    break
            except:
                pass
    except:
        print("프로그램을 다시 시작해주세요")
    for tmp in datadictBySex.keys():
        if datadictBySex[tmp] == '0':
            print(tmp, " parsing error ", end='')
            datadictBySex[tmp] = input("input ::")
    #if len(datadictBySex) != 4:
     #   print("::: 성별그래프 겹침 발견 데이터확인필요 아래에서 누락 점검")
      #  print(datadictBySex)
    print(">>> 왼쪽아래 추출 종료")
    # 오른쪽아래
    print(">>> 오른쪽아래 추출 시작")
    datadictByAge = {'0~12desktop': '0', '0~12mobile': '0', '13~19desktop': '0', '13~19mobile': '0', '20~24desktop': '0', '20~24mobile': '0', '25~29desktop': '0', '25~29mobile': '0', '30~39desktop': '0', '30~39mobile': '0', '40~49desktop': '0', '40~49mobile': '0', '50~desktop': '0', '50~mobile': '0'}
    idx = 0
    try:
        for test in driver.find_elements_by_tag_name('rect')[10:]:
            try:
                hover = ActionChains(driver).move_to_element(test)
                hover.perform()
                tmp = driver.find_element_by_tag_name('path')
                hovertmp = ActionChains(driver).move_to_element(tmp)
                hovertmp.perform()
                hovertmp.click()
                time.sleep(0.5)
                bs4 = BeautifulSoup(driver.page_source, "lxml")
                div = bs4.find('div', id='highcharts-6').find('div',class_='highcharts-tooltip')
                if '~' in div.get_text():
                    key, data = str(div.get_text()).split(':')
                    datadictByAge[key]=data
            except:
                pass

    except:
        print("none 월간 검색수 사용자 통계 (최근일 기준) / 나이대(%) data")
    for tmp in datadictByAge.keys():
        if datadictByAge[tmp] == '0':
            print(tmp, " parsing error ", end='')
            datadictByAge[tmp] = input("input ::")
    #if len(datadictByAge) != 14:
        #print("::: 나이그래프 겹침 발견 데이터확인필요 아래에서 누락 점검 ")
        #print(datadictByAge)
    print(">>> 오른쪽아래 추출 종료")
    #datadictBySex = sorted(datadictBySex.items(), key=operator.itemgetter(0))
    #datadictByAge = sorted(datadictByAge.items(), key=operator.itemgetter(0))
    print(datadic)
    print(datadictBySex )
    print(datadictByAge)
    # file
    pc = int(pc)
    mobile = int(mobile)
    with open(title+'.csv','w') as f:
        for tmp in datadic.keys():
            f.write(tmp+',')
        f.write('\n')
        for tmp in datadic.keys():
            f.write(str(datadic[tmp]).replace(',','')+',')
        f.write('\n')
        ##
        for tmp in datadictBySex.keys():
            f.write(tmp+',')
        f.write('\n')
        for tmp in datadictBySex.keys():
            f.write(datadictBySex[tmp]+'%,')
        f.write('\n')
        for tmp in datadictBySex.keys():
            if 'mobile' in tmp:
                f.write(str(round((mobile*float(datadictBySex[tmp]))/100.0))+',')
            else:
                f.write(str(round((pc * float(datadictBySex[tmp])) / 100.0)) + ',')
        f.write('\n')
        ##
        for tmp in datadictByAge.keys():
            f.write(tmp+',')
        f.write('\n')
        for tmp in datadictByAge.keys():
            f.write(datadictByAge[tmp]+'%,')
        f.write('\n')
        for tmp in datadictByAge.keys():
            if 'mobile' in tmp:
                f.write(str( round((mobile*float(datadictByAge[tmp]))/100.0))+',')
            else:
                f.write(str(round((pc * float(datadictByAge[tmp])) / 100.0)) + ',')
        f.write('\n')
