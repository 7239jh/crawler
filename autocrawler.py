import sys, os
import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, date
import time
from tqdm import tqdm
import pandas as pd

sleep_sec = 0.5


def crawling_main_image(url):  # 이미지URL 수집
    sys.setrecursionlimit(10000)
    headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    soup=soup.find_all('div',class_='nbd_a _LAZY_LOADING_ERROR_HIDE')
    image1=[a.find('img',class_='_LAZY_LOADING') for a in soup]
    
    l=[]
    for i in image1 :
        imgUrl=i['data-src'] 
        if 'w647' in imgUrl:
            l.append(imgUrl)
    return l


def crawling_main_press(url):  # 언론사명 수집
    sys.setrecursionlimit(10000)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    soup=soup.find('div',class_='media_end_head_top')
    press=soup.find('img')['title']

    return press

def crawling_main_date(url): # 기사작성, 수정 날짜 수집
    sys.setrecursionlimit(10000)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    text=soup.find_all('div',class_='media_end_head_info_datestamp_bunch')
    b=[a.find('span','media_end_head_info_datestamp_time') for a in text]
    
    t=[]
    for i in b:
            i=i.text
            t.append(i)
    return(t)


def crawling_main_title(url):  # 기사 제목 수집
    sys.setrecursionlimit(10000)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    text=soup.find('div',class_='media_end_head_title').text
    return text.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')


def crawling_main_text(url):  # 기사 본문 수집
    sys.setrecursionlimit(10000)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    text=soup.find('div',{'id' : 'dic_area'}).text
    return text.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')


def crawling_main_reporter(url): # 작성자명 수집
    sys.setrecursionlimit(10000)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36" }

    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    try:
        return soup.find('div',class_='byline').text.lstrip()
    except:
        return []

    
    
def regex(x):  # 간단한 전처리 정규식
    
    x=x.replace('<span class="t11">','')
    x=x.replace('</span>','')
    x=x.replace('<div class="journalistcard_summary_name">','')
    x=x.replace('</div>','') 
    x= re.sub('[-=+#/\?^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》▷]', '', x)
    return x
    
    
    ###############크롤러 함수####################

def crawler():
    classes=  [259,258,230]# 259=금융, 258=증권, 230=IT일반
    section=[101,101,105]# 정치=100, 경제=101, 사회=102, 생활/문화=103, it/과학=105, 세계=104
    loadname=['금융','증권','IT일반']
    yesterday= date.today()-timedelta(1)
    dates=yesterday.strftime("%Y%m%d")
    
    for c in zip(classes,section, loadname):
    
        chrome_path ='D:/chromedriver/chromedriver.exe' #크롬드라이버 경로
        browser = webdriver.Chrome(chrome_path)
        news_url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={}&sid1={}&date={}'.format(c[0],c[1],dates)
        browser.get(news_url)
        time.sleep(sleep_sec)
        news_dict = {}
        cur_page = 1
        idx=1
        pbar = tqdm(leave = True)
    
        
        for i in range(300):
            table = browser.find_element_by_xpath('//div[@class="list_body newsflash_body"]')
            table2 = table.find_element_by_xpath('./ul[@class="type06_headline"]')
            try:
                table3= table.find_element_by_xpath('./ul[@class="type06"]')
            except:
                pass
            li_list1= table2.find_elements_by_xpath('./li') 
            try:
                li_list2= table3.find_elements_by_xpath('./li')
            except:
                pass
            dl_list1= [li.find_element_by_xpath('./dl') for li in li_list1]
            try:
                dl_list2= [li.find_element_by_xpath('./dl') for li in li_list2]
            except:
                pass
            dt_list1= [dl.find_element_by_xpath('./dt') for dl in dl_list1]
            try:
                dt_list2= [dl.find_element_by_xpath('./dt') for dl in dl_list2]
            except:
                pass
            a_list1= [dt.find_element_by_xpath('./a') for dt in dt_list1]
            try:
                a_list2= [dt.find_element_by_xpath('./a') for dt in dt_list2]
            except:
                pass
            try:
                a_list=a_list1+a_list2
            except:
                a_list=a_list1
        
        
            for n in a_list[:len(a_list)]:
                try:
                    url = n.get_attribute('href')
                
                    news_dict[idx] = {'date': crawling_main_date(url),
                                  'title' :crawling_main_title(url) ,
                                'url' : url,
                                'section': c[2],
                                'text' : crawling_main_text(url).lstrip(),
                                'image': crawling_main_image(url),
                                'press':crawling_main_press(url),
                                'reporter':crawling_main_reporter(url)}
                except:
                    pass
                try:
                    print(crawling_main_title(url))   # 수집 할 때 마다 타이틀 출력
                except:
                    pass
                idx +=1
                pbar.update(1)
                time.sleep(2)
                news_df = DataFrame(news_dict).T
                folder_path = os.getcwd()
                xlsx_file_name = 'news_{}_{}.xlsx'.format(c[2],dates)  
                news_df.to_excel(xlsx_file_name,index=False)   # 인덱스 제거하고 엑셀로 변환 
                print('저장경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))
                    
                os.startfile(folder_path)                
    
            cur_page +=1
            
            if (cur_page-1)%10 == 0:
                pages = browser.find_element_by_xpath('//div[@class="paging"]')
                
                if len(pages.find_elements_by_xpath('.//a'))<10:
                    pbar.close()
                    print('\n브라우저 종료\n' + '=' * 100)
                    time.sleep(0.7)
                    browser.close()
                    break  
                elif len(pages.find_elements_by_xpath('.//a'))==10:
                    if pages.find_elements_by_xpath('.//a')[-2].text==str(9):
                        next_page_url = pages.find_elements_by_xpath('.//a')[-1].get_attribute('href')
                        browser.get(next_page_url)
                        time.sleep(sleep_sec)
                    else:
                        pbar.close()
                        print('\n브라우저 종료\n' + '=' * 100)
                        time.sleep(0.7)
                        browser.close()
                        break                      
                else:
                    next_page_url = pages.find_elements_by_xpath('.//a')[-1].get_attribute('href')
                    browser.get(next_page_url)
                    time.sleep(sleep_sec)
                                   
            else:
                pages = browser.find_element_by_xpath('//div[@class="paging"]')
                if len([p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)])==1:
                   next_page_url = [p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)][0].get_attribute('href')    
                   browser.get(next_page_url)   
                   time.sleep(sleep_sec)
                else:
                    pbar.close()
                    print('\n브라우저 종료\n' + '=' * 100)
                    time.sleep(0.7)
                    browser.close()
                    break              
      
                    
    