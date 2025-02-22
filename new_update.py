import os
import json
import requests
import html
import re
from datetime import datetime

# 검색어
search = "반도체"
display = 20
sort = "sim"


# 네이버 developer에서 발급 "https://developers.naver.com/apps/#/myapps/5_EbG5C0vaQvkusHOlP5/overview"
client_id = "secrets.client_id"
client_secret = "secrets.client_secret"

# url = "https://openapi.naver.com/v1/search/{검색}.json" 검색에 blog, news, 등에 따라 검색할 종목 변경

url = "https://openapi.naver.com/v1/search/news.json"

# API 인증을 위한 Id와 Secret을 headers에 입력
headers = {
    "X-Naver-Client-Id" : client_id,
    "X-Naver-Client-Secret" : client_secret
}

# 검색어, 표시할 뉴스의 수, 정렬기준을 위한 파라미터 설정(display의 경우 int형 숫자로 입력받기 때문에 string 형태로 변환)
params = {
    "query" : search,
    "display" : str(display),
    "sort" : sort
}

# 설정한 headers와 params를 get을 통해 url에 있는 사이트에 요청
response = requests.get(url, headers=headers, params=params)

# 만약, url에 정상적으로 요청을 받는다면 .status_code == 200
if(response.status_code==200):

    # json을 dictionary 타입으로 변환
    response_dict = response.json()
    
    for item in response_dict["items"]:
        
        # response_dict에 존재하는 html entity 변환
        # html.unescape()를 사용하여 html 엔티티를 원래 문자로 변환
        item["title"] = html.unescape(item["title"])
        item["description"] = html.unescape(item["description"])
        

        # re.sub()를 사용하여 html 태그 제거
        # re.sub(pattern, replacement, string) => pattern에 해당하는 부분을 replacement로 바꾼다.
        # r"<.*?>" => r : raw string으로 \를 특수문자가 아닌 string으로 해석, <>사이의 모든 문자열을 찾는다.
        # . : 아무 문자 하나
        # * : 0번 이상 반복
        # ? 최소로 찾는다(<로 시작해서 가장 가까운 >를 찾는다)
        # ex) text = <b>안녕</b> <i>하세요</i> => re.sub(r"<.*?>", "", text) => 안녕하세요
        item["title"] = re.sub(r"<.*?>", "", item["title"])
        item["description"] = re.sub(r"<.*?>", "", item["description"])

        # 문자열을 datetime으로 변환 후 datetime을 다시 문자열로 출력 
        item["pubDate"] = datetime.strptime(item["pubDate"], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H시 %M분')
    
else:
    print(f"Error Code: {response.status_code}")

