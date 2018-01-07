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
    print(">>> Made By Pakr HyungJune copyright @ DevHyung")
    with open('data.csv', 'w') as f:
        while True:
            # Setting variable
            print("_" * 50)
            print(">>> Loding....")
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
            # 이부분을 수정 하면 됌 내꺼는 2
            driver.switch_to.window(driver.window_handles[2])
            # Login end
            title = ""
            # if event evoke, parsing start
            k = input(">>> 키워드를 입력하세요 ::")
            driver.find_element_by_xpath('//*[@id="wrap"]/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div[2]/form/div[1]/div/div/textarea').send_keys(k)
            driver.find_element_by_xpath('//*[@id="wrap"]/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div[2]/form/div[4]/div/div/ul/li/button').click()
            print("\t>>> 아래에 조회 결과중 추출하고픈 정확한 이름을 입력하세요")
            key = input("\t>>> 입력 ::")
            tmpkey = key
            bs4 = BeautifulSoup(driver.page_source, "lxml")
            try:
                tr = bs4.find('table',class_='table table-bordered').find_all('tr')
                for tmp in tr[2:]:
                    if key == tmp.find('span',class_='keyword').get_text().strip():#같은경우
                        pc = int(tmp.find_all('td',class_=' text-right txt-r')[0].get_text().replace(',',''))
                        mobile = int(tmp.find_all('td', class_=' text-right txt-r')[1].get_text().replace(',',''))
                        pc_click = float(tmp.find_all('td', class_=' text-right txt-r')[2].get_text().replace(',',''))
                        mobile_click = float(tmp.find_all('td', class_=' text-right txt-r')[3].get_text().replace(',',''))
                        break
            except:
                print(">>> 정확한 이름을 입력해주세요 !")
                exit(-1)
            driver.find_element_by_xpath('//*[@id="wgt-'+key+'"]/td[2]/span/span').click()
            time.sleep(2)

            bs4 = BeautifulSoup(driver.page_source,"lxml")
            table = bs4.find('table',class_="layout-table")
            path = table.find('g',class_="highcharts-markers highcharts-series-0 highcharts-tracker")
            pathlist = path.find_all('path')

            title = bs4.find('h4',class_='modal-title').find('span',class_='ng-binding').get_text()
            #print(pathlist)
            now = driver.current_window_handle
            driver.switch_to.window(now)
            #꺾은선
            print("\t>>> 꺾은선 추출 시작")
            datadic = dict([('2017-01desktop', '-1'), ('2017-01mobile', '-1'), ('2017-02desktop', '-1'), ('2017-02mobile', '-1'), ('2017-03desktop', '-1'), ('2017-03mobile', '-1'), ('2017-04desktop', '-1'), ('2017-04mobile', '-1'), ('2017-05desktop', '-1'), ('2017-05mobile', '-1'), ('2017-06desktop', '-1'), ('2017-06mobile', '-1'), ('2017-07desktop', '-1'), ('2017-07mobile', '-1'), ('2017-08desktop', '-1'), ('2017-08mobile', '-1'), ('2017-09desktop', '-1'), ('2017-09mobile', '-1'), ('2017-10desktop', '-1'), ('2017-10mobile', '-1'), ('2017-11desktop', '-1'), ('2017-11mobile', '-1'), ('2017-12desktop', '-1'), ('2017-12mobile', '-1')])
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
                if datadic[tmp] == '-1' and 'mobile' in tmp:
                    print("\t\t",tmp, " parsing error ", end='')
                    datadic[tmp] = input("input ::")
            #if len(datadic) != 24:
             #   print("::: 그래프 겹침 발견 데이터확인필요 아래에서 누락 점검")
              #  print(datadic)
            print("\t>>> 꺾은선 추출 종료")
            #왼쪽아래 막대
            print("\t>>> 성별 추출 시작")
            idx = 0
            datadictBySex = {'남성desktop': '-1', '남성mobile': '-1', '여성desktop': '-1', '여성mobile': '-1'}
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
                if 'COMMON.TERM' in tmp:
                    break
                if datadictBySex[tmp] == '-1':
                    print("\t\t",tmp, " parsing error ", end='')
                    datadictBySex[tmp] = input("input ::")
            #if len(datadictBySex) != 4:
             #   print("::: 성별그래프 겹침 발견 데이터확인필요 아래에서 누락 점검")
              #  print(datadictBySex)
            print("\t>>> 성별 추출 종료")
            # 오른쪽아래
            print("\t>>> 나이별 추출 시작")
            datadictByAge = {'0~12desktop': '-1', '0~12mobile': '-1', '13~19desktop': '-1', '13~19mobile': '-1', '20~24desktop': '-1', '20~24mobile': '-1', '25~29desktop': '-1', '25~29mobile': '-1', '30~39desktop': '-1', '30~39mobile': '-1', '40~49desktop': '-1', '40~49mobile': '-1', '50~desktop': '-1', '50~mobile': '-1'}
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

                if datadictByAge[tmp] == '-1':
                    print("\t\t",tmp, " parsing error ", end='')
                    datadictByAge[tmp] = input("input ::")
            #if len(datadictByAge) != 14:
                #print("::: 나이그래프 겹침 발견 데이터확인필요 아래에서 누락 점검 ")
                #print(datadictByAge)
            print("\t>>> 나이별 추출 종료")
            print("\t>>> "+tmpkey+" 추출종료 ")
            #datadictBySex = sorted(datadictBySex.items(), key=operator.itemgetter(0))
            #datadictByAge = sorted(datadictByAge.items(), key=operator.itemgetter(0))
            #print(datadic)
            #print(datadictBySex )
            #print(datadictByAge)
            # file
            pc = int(pc)
            mobile = int(mobile)

            # 열1
            f.write(tmpkey+",")
            #PC+모바일 (합산)
            f.write(str(pc+mobile)+",")
            #pc
            f.write(str(pc)+",")
            #mobile
            f.write(str(mobile)+",")
            #월평균 클릭수 pc,mobile
            f.write(str(pc_click)+",")
            f.write(str(mobile_click)+",")
            # 월간검색수 사용자 통계
            # 남성 (pc,mobile) , 여성(pc,mobile)순
            for tmp in datadictBySex.keys():
                f.write(datadictBySex[tmp]+'%(')
                if 'mobile' in tmp:
                    f.write(str(round((mobile*float(datadictBySex[tmp]))/100.0))+'명),')
                else:
                    f.write(str(round((pc * float(datadictBySex[tmp])) / 100.0)) + '명),')
            # 월간검색수 사용자 통게 나이순
            for tmp in datadictByAge.keys():
                f.write(datadictByAge[tmp]+'%(')
                if 'mobile' in tmp:
                    f.write(str(round((mobile * float(datadictByAge[tmp])) / 100.0)) + '명),')
                else:
                    f.write(str(round((pc * float(datadictByAge[tmp])) / 100.0)) + '명),')
            # 월별검색수 추이 (모바일만 )
            for tmp in datadic.keys():
                if "mobile" in tmp:
                    f.write(str(datadic[tmp]).replace(',','')+',')
            f.write('\n')

            driver.quit()
            cont = str(input(">>> 계속하려면 1, 종료는 0 ::"))
            print("_" * 50)
            if cont == '0':
                break

