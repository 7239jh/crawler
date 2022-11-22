# crawler 
cnn의 과거 원하는 년도와 월의 모든 기사를 크롤링하여 파일로 저장

## 년도 및 월 설정 
```python
years=[2020,2021,....]
months= ['01','02','03','04','05','06','07','08','09','10','11','12']
```
위의 리스트에 원하는 년도와 월 입력

## 크롬 드라이버 경로 지정
본인 크롬버전에 맞는 크롬드라이버를 설치 후 경로 입력
```python
chrome_path ='D:/chromedriver/chromedriver.exe' #크롬드라이버 경로
```

## 수집 데이터 종류 
date: 기사 날짜  
title: 기사 제목  
url: 기사 url  
section: 섹션구분이 없음  
text: 기사 본문  
image: 이미지 url  
press: 기사 언론사  
reporter: 기사 작성자  

```python
news_dict[idx]={'date':span[0].text,
                'title':str(span[1].text),
                'url':n_url,
                'section':'not',
                'text':crawling_main_text(n_url),
                'image':crawling_main_iamge(n_url),
                'press':'CNN',
                'reporter':crawling_main_reporter(n_url),
                 }
```
수집을 원하지 않는 데이터는 위에서 지우면 된다.

## 수집 데이터 파일로 저장
```python
xlsx_file_name = 'D:/크롤링/안보뉴스/CNN/CNN_news_{}_{}.xlsx'.format(y,m)
news_df.to_excel(xlsx_file_name,index=False)   # 인덱스 제거하고 엑셀로 변환 
print('엑셀 저장 완료 | 경로 : {}\n'.format(xlsx_file_name))               
```
꼭 엑셀로 저장 안해도 가능, 원하는 파일로 변경

## 실행 방법
터미널에서 cnn_crawler.py가 설치된 폴더로 경로 이동 후 아래 입력
```
python cnn_crawler.py
```
