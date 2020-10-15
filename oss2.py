import requests
from bs4 import BeautifulSoup

import json
import webbrowser as w

import time

import msvcrt as m
from selenium import webdriver
from seleniumrequests import Chrome
options = webdriver.ChromeOptions()
options.headless = True
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

custom_header = {'POST':'/std/cps/inqire/AtnlcScreSungjukInfo.do HTTP/1.1',
'Host': 'klas.kw.ac.kr',
'Connection': 'Keep-Alive',
'Content-Length': '0',
'Accept': 'application/json, text/plain, */*',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
'Content-Type': 'application/json; charset=UTF-8',
'Origin': 'https://klas.kw.ac.kr',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreStdPage.do',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}
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
cookies = browser.get_cookies()

s = requests.Session()
s.headers.update(custom_header)
for cookie in cookies :
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)
# 수강 성적 데이터 서버에 요청 1
sungjuk_res = s.post(base_url+'std/cps/inqire/AtnlcScreSungjukInfo.do')
#print(sungjuk_res.text)
'''
print(type(sungjuk_res.text)) # string
print(type(sungjuk_res.json())) # list
'''
sungjuk_data = sungjuk_res.json()
'''
print(type(sungjuk_data[0])) # dict
print(type(sungjuk_data[0]['sungjukList'])) # list
print(type(sungjuk_data[0]['sungjukList'][0]))
'''
print(sungjuk_data[0]['sungjukList'][0])
browser.quit()

