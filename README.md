# crawler
스케줄러를 사용하여 원하는 시간에 원하는 섹션의 네이버 뉴스를 전부 크롤링하여 파일로 저장

## 섹션 변경 및 날짜 설정
|상위섹션|하위섹션|
|---|---|
|정치=100|대통령실=264, 국회/정당=265, 북한=268, 행정=266, 국방/외교=267, 정치일반=269|
|경제=101|금융=259,증권=258,산업/재계=261,중기/벤처=771,부동산=260,글로벌 경제=262,생활경제=310,경제 일반=263|
|사회=102|사건사고=249, 교육=250, 노동=251, 언론=254, 환경=252, 인권/복지=59b, 식품/의료=255, 지역=256, 인물=276, 사회일반=257|
|생활/문화=103|건강정보=241, 자동차/시승기=239, 도로/교통=240, 여행/레저=237, 음식/맛집=238, 패션/뷰티=376, 공연/전시=242, 책=243, 종교=244, 날씨=248, 생활문화일반=245|
|IT/과학=105|모바일=731, 인터넷/SNS=226, 통신/뉴미디어=227, IT일반=230, 보안/해킹=732, 컴퓨터=283, 게임/리뷰=229, 과학 일반=228|
|세계=104|아시아/호주=231, 미국/중남미=232, 유럽=233, 중동/아프리카=234, 세계 일반=322|

```python
classes=  [259,258,230]# 259=금융, 258=증권, 230=IT일반
section=[101,101,105]# 정치=100, 경제=101, 사회=102, 생활/문화=103, it/과학=105, 세계=104
loadname=['금융','증권','IT일반']
yesterday= date.today()-timedelta(1)
dates=yesterday.strftime("%Y%m%d")
```
매일 전날의 뉴스를 수집하기 위해 어제날짜로 설정

## 크롬 드라이버 경로 지정
본인 크롬버전에 맞는 크롬드라이버를 설치 후 경로 입력
```python
chrome_path ='D:/chromedriver/chromedriver.exe' #크롬드라이버 경로
```

## 수집 데이터 종류 
date: 기사 날짜  
title: 기사 제목  
url: 기사 url  
section: 수집한 기사의 세부섹션  
text: 기사 본문  
image: 이미지 url  
press: 기사 언론사  
reporter: 기사 작성자  
```python
news_dict[idx] = {'date': crawling_main_date(url),
                'title' :crawling_main_title(url) ,
                'url' : url,
                'section': c[2],
                'text' : crawling_main_text(url).lstrip(),
                'image': crawling_main_image(url),
                'press':crawling_main_press(url),
                'reporter':crawling_main_reporter(url)}
```
수집을 원하지 않는 데이터는 위에서 지우면 된다.

## 수집 데이터 파일로 저장
```python
xlsx_file_name = 'news_{}_{}.xlsx'.format(c[2],dates)  
news_df.to_excel(xlsx_file_name,index=False)   # 인덱스 제거하고 엑셀로 변환 
print('저장경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))
```
꼭 엑셀로 저장 안해도 가능 원하는 파일로 변경

## 수집 시간 설정
```python
schedule.every().day.at('16:00').do(crawler)
```
## 실행 방법
터미널에서 autocrawler.py와 schedule_every.py가 설치된 폴더로 경로 이동 후 아래 입력
```
python schedule_every.py
```






