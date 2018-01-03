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
from bs4 import BeautifulSoup
from CONFIG import *
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
    # Login end
    input("현재페이지를 가져오시겠습니까 ? :: ")
    bs4 = BeautifulSoup(driver.page_source,"lxml")
    print(bs4.prettify())
    "https://manage.searchad.naver.com/customers/1316664/tool/keyword-planner"