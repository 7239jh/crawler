import sys, os
import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle, progressbar, json, glob, time
from tqdm import tqdm
import pandas as pd
import argparse
import ast

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분'
sleep_sec = 0.5

def crawling_main_text(url):  # 기사 본문 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',{'class':'article-body__content'})
    soup2=soup1.find_all('p',class_='')
    texts=[]
    for i in soup2:
        i=i.text
        i.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')
        i= re.sub('\xa0','',i)
        i= re.sub('[\'\']','',i)
        texts.append(i) 
    return str(texts)  

def crawling_main_iamge(url):  # 기사 이미지 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',{'class':'article-body__content'})
    soup2=soup1.find('img')
    return str(soup2['src'])
 
def crawling_main_date(url):  # 기사 날짜 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',class_='article-body__date-source')
    return str(soup1.text)

def crawling_main_reporter(url):  # 기사 작성자 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',class_='article-inline-byline')
    return str(soup1.text)

years=[2012,2013]
months=['january','february','march','april','may','june','july','august','september','october','november','december']

for y in years:
    for m in months:
        chrome_path = 'D:/chromedriver/chromedriver.exe' 
        browser = webdriver.Chrome(chrome_path)
        news_url = 'https://www.nbcnews.com/archive/articles/{}/{}'.format(y,m)
        browser.get(news_url)
        time.sleep(sleep_sec)
        news_dict = {}
        idx=1
        pbar = tqdm(leave = True)

        tabl = browser.find_element_by_xpath('//main[@class="MonthPage"]')
        a= tabl.find_elements_by_xpath('./a') 
        for i in a:
            try:
                n_url=i.get_attribute('href')
                news_dict[idx]={'date': crawling_main_date(n_url),
                                'title' :str(i.text),
                                'url' : str(n_url),
                                'section': 'not',
                                'text' : crawling_main_text(n_url).lstrip(),
                                'image': crawling_main_iamge(n_url),
                                'press':'NBC',
                                'reporter':crawling_main_reporter(n_url)}
            except:
                pass
            idx +=1
            pbar.update(1)
            news_df = DataFrame(news_dict).T
            xlsx_file_name = 'D:/NBC/nbc_news_{}_{}.xlsx'.format(y,m)
            news_df.to_excel(xlsx_file_name,index=False)   
            print('엑셀 저장 완료 | 경로 : {}\n'.format(xlsx_file_name))