import requests
from urllib import request
from bs4 import BeautifulSoup
import time
import random

# URL 설정
BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
ARTICLE_BASE_URL = "https://gall.dcinside.com"
# 헤더 설정
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}
# 갤러리 설정
g_id = '갤러리이름'
# 검색어 설정
s_keyword = '검색어'
# 식별 코드 설정
idcode = '식별코드'
# 시작점 설정
search_pos = -777777
# 검색 범위 설정 단위: 만
limit_range = 7 
# 게시물 카운트
cnt = 1

# 결과물 파일 생성
f = open("output.txt", 'w', encoding="UTF-8")

for i in range(0, limit_range):
    init_params = {'id': g_id, 'page': 1, 'search_pos': search_pos, 's_type': 'search_name', 's_keyword': s_keyword}
    init_response = requests.get(BASE_URL, params=init_params, headers=header)
    init_soup = BeautifulSoup(init_response.content, 'html.parser')

    # 페이지 마지막 번호 찾기
    page_end = init_soup.find('a', class_='sp_pagingicon page_end')
    href = page_end['href']
    page_end_idx = int(href.split("page=")[1].split("&")[0])

    # 1페이지 부터 end 페이지 까지 탐색
    for j in range(1, page_end_idx):
        params = {'id': g_id, 'page': j, 'search_pos': search_pos, 's_type': 'search_name', 's_keyword': s_keyword}
        response = requests.get(BASE_URL, params=params, headers=header)

        soup = BeautifulSoup(response.content, 'html.parser')

        article_list = soup.find('tbody').find_all('tr')

        print(str(i) + " : " + str(j) + "/" + str(page_end_idx))
        for tr_item in article_list:
            # 식별 코드 추출
            element = tr_item.find('td', class_='gall_writer ub-writer')
            data_uid = element.get('data-uid')

            # 식별 코드가 일치할 경우 출력
            if data_uid == idcode:
                title_tag = tr_item.find('a', href=True)
                title = title_tag.text

                data = "[" + str(cnt) + "] " + title + '\n' + ARTICLE_BASE_URL + title_tag['href'] + '\n'
                cnt += 1
                f.write(data)

                print("제목: ", title)
                print("주소: ", title_tag['href'])
        # 2 - 4초 딜레이
        time.sleep(random.uniform(2, 4))
    # 검색 범위 이동
    search_pos += 10000
f.close()