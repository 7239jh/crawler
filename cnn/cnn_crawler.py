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
sleep_sec = 0.2

def crawling_main_text(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',{'class':'article__content-container'})
    if soup1==None:
        return 'not'
    else:
        soup2=soup1.find_all('p',class_='paragraph inline-placeholder')   
        if soup2 ==None:
            return 'not'
        else:
            texts=[]
            for i in soup2:
                i=i.text
                i.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')
                i= re.sub('\xa0','',i)
                i= re.sub('[\'\']','',i)
                i= re.sub('\\n  ','',i)
                i= re.sub('  ','',i)
                texts.append(i) 
            return texts

def crawling_main_iamge(url):  # 기사 이미지 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',{'class':'image__lede article__lede-wrapper'})
    if soup1==None:
        return 'not'
    else:
       soup2=soup1.find('img')
       if soup2==None:
           return 'not'
       else:
        return soup2['src']
    
def crawling_main_reporter(url):  # 기사 작성자 수집
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup1=soup.find('div',class_='byline__names')
    if soup1==None:
        return 'not'
    else:
        i=soup1.text
        i=re.sub('\n','',i)    
        i=re.sub('\t','',i) 
        return i

years=[2020,2021]
months= ['01','02','03','04','05','06','07','08','09','10','11','12']
#months=['03']
for y in years:
    for m in months:
        chrome_path = 'D:/chromedriver/chromedriver.exe' 
        browser = webdriver.Chrome(chrome_path)
        news_url = 'https://edition.cnn.com/article/sitemap-{}-{}.html'.format(y,m)
        browser.get(news_url)
        time.sleep(sleep_sec)
        news_dict={}
        idx=1
        pbar = tqdm(leave = True)
        text=browser.find_elements_by_xpath('//div[@class="sitemap-entry"]')
        ul=text[1].find_element_by_xpath('./ul')
        li=ul.find_elements_by_xpath('./li')
        for i in li:
            span=i.find_elements_by_xpath("./span")
            n_url=span[1].find_element_by_xpath("./a").get_attribute('href')
            news_dict[idx]={'date':span[0].text,
                            'title':str(span[1].text),
                            'url':n_url,
                            'section':'not',
                            'text':crawling_main_text(n_url),
                            'image':crawling_main_iamge(n_url),
                            'press':'CNN',
                            'reporter':crawling_main_reporter(n_url),
                            }
            idx +=1
            pbar.update(1)
            news_df = DataFrame(news_dict).T
            xlsx_file_name = 'D:/CNN/CNN_news_{}_{}.xlsx'.format(y,m)
            news_df.to_excel(xlsx_file_name,index=False)  
            print('엑셀 저장 완료 | 경로 : {}\n'.format(xlsx_file_name))               
