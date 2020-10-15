import requests
from bs4 import BeautifulSoup

import json
import webbrowser as w

import time

import msvcrt as m
from selenium import webdriver

options = webdriver.ChromeOptions()
#options.headless = True
options.add_argument("window-size=2560x1600")
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 기본 도메인
base_url = "https://klas.kw.ac.kr/"
# ==================== STEP 1 KLAS 로그인 ==================== 
    # 로그인 정보 입력 받기(ID)
user_id = input("학번을 입력하세요:")
print("비밀번호를 입력하세요:",end='',flush=True)
    # 로그인 정보 입력 받기(PW)
user_pw = ''
    # 패스워드 입력시 *로 표기(BS,Enter 구현)
buf = ''
while True:
    ch = m.getch()
    if ord(ch) == 13 :
        print('')
        break
    elif ord(ch) == 8:
        if len(buf)>1 :
            buf = buf[:-1]
            print('\r'+"비밀번호를 입력하세요:"+' '*(len(buf)+1),end='',flush=True)
            print('\r'+"비밀번호를 입력하세요:"+'*'*len(buf),end='',flush=True)
            continue
        else :
            buf = ''
            print('\r'+"비밀번호를 입력하세요:"+' '*(len(buf)+1),end='',flush=True)
            print('\r'+"비밀번호를 입력하세요:",end='',flush=True)
            continue
    else :
        ch = (str(ch))
        buf += ch[2:-1]
        print('*',end='',flush=True)
user_pw = buf

    # Selenium으로 로그인
browser = webdriver.Chrome("./chromedriver.exe",options=options)
browser.get(base_url)
elem = browser.find_element_by_id("loginId")
elem.send_keys(user_id)
elem = browser.find_element_by_id("loginPwd")
elem.send_keys(user_pw)
elem = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/form/div[2]/button")
elem.click()
elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='appModule']/div/div[1]/div[1]/select")))
'''
# ==================== STEP 2 현재 학기 과목 확인 ==================== 
main_url = browser.current_url
soup = BeautifulSoup(browser.page_source,"lxml")

subjects = soup.find('ul',attrs={'class':'subjectlist listbox'})

tag = soup.find_all("p",attrs={'class':'title-text'})

print(tag[0].get_text().strip())
for subject in subjects :
    title = subject.find("div",attrs={'class':'left'}).get_text().strip()
    print(title)

'''
#숨김 메뉴 보이기
elem = browser.find_element_by_class_name("navbar-toggler-icon")
elem.click()
time.sleep(3)
# ==================== STEP 3 수강중인 과목 확인 ==================== 
elem = browser.find_element_by_xpath("//*[@id='navbarHeader']/div/div/div[1]/ul/li[2]/ul/li[2]/a") # 수강/성적 조회 버튼 찾기
elem.click()
time.sleep(2)
#elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='appModule']")))
soup = BeautifulSoup(browser.page_source,"lxml")
sungjuk_tags = soup.find_all('th')
sungjuk_list = soup.find_all('td')
tag_count=0
data_count=0
for sungjuk in sungjuk_list[34:] :
                if sungjuk.get_text().strip().startswith("예비") :
                    break
                if data_count > 0 and data_count%8==0:
                    print(sungjuk.get_text().strip().center(8))
                    data_count=0
                    tag_count+=1
                else :
                    print(sungjuk.get_text().strip().center(8),sep=' ',end='')
                    data_count+=1   
'''
for sungjuk_tag in sungjuk_tags[28:] :
    if sungjuk_tag.get_text().strip().endswith("학기"):
        print()
        print(sungjuk_tag.get_text().strip())
        continue
    elif sungjuk_tag.get_text().strip().startswith("프로그램"):
        break
    else :
        if sungjuk_tag.get_text().strip().endswith("삭제여부"):
            print(sungjuk_tag.get_text().strip().center(8))
            data_count=0
            for sungjuk in sungjuk_list[34:] :
                if sungjuk.get_text().strip().startswith("예비") :
                    break
                if data_count > 0 and data_count%8==0:
                    print(sungjuk.get_text().strip().center(8))
                    data_count=0
                    tag_count+=1
                else :
                    print(sungjuk.get_text().strip().center(8),sep=' ',end='')
                    data_count+=1   
            continue            
        else:
            print(sungjuk_tag.get_text().strip().center(8),sep=' ',end='')
            tag_count+=1
'''
browser.quit()

