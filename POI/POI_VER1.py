
#특정 poi를 긁어오기위해 kakao map을 활용했습니다
# https://apis.map.kakao.com/
# https://apis.map.kakao.com/web/documentation/#CategoryCode
# * 트래킹 제한: 1일 300,000회 사용가능합니다


import requests
import folium
import collections
from tinydb import TinyDB,Query
import pandas as pd

# # 잘작동 되는지 확인용 (Test)
# # kakao api 사용하기 위한 key
app_key = 'KakaoAK' + 'f7dea420445453a99101987bcf736ac3'
url = 'https://dapi.kakao.com/v2/local/search/category.json'
# params = {
#     'category_group_code' : 'FD6',
#     'page': 1,
#     'rect': '127.0085280000,37.5357715389,127.1221115536,37.4573204481',
# }
# headers  = {
#     'Authorization': 'KakaoAK f7dea420445453a99101987bcf736ac3'
# }
# resp = requests.get(url, params=params, headers=headers)
# # 바이트 → 문자열 → JSON
# # resp.json()을 쓰면 내부적으로 utf-8로 디코딩해서 dict로 반환
# data = resp.json()
# # 카카오 로컬 API 기준: 'documents' key에 장소 정보 리스트
# documents = data['documents']
# # 확인~~
# df = pd.DataFrame(documents)
# print(df.head())

print("##########***************##################")

## 용두동 좌표
start_x, start_y = 127.02, 37.57
end_x, end_y = 127.04, 37.59

##함수만들어서 사용하고자함
##
def get_store_list(start_x, start_y, end_x, end_y):
    offset = 0.000005
    cnt = 1
    resp_list = []

    while True:
        params = {
            'category_group_code': 'FD6',
            'page': cnt,
            'rect': f'{start_x-offset},{start_y-offset},{end_x+offset},{end_y+offset}'
        }
        headers = {'Authorization': app_key}
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()

        # 예외처리
        if 'meta' not in data:
            print("⚠️ API 응답 오류:", data)
            break

        search_count = data['meta'].get('total_count', 0)
        print(f"page {cnt}, count={search_count}")

        # 🔸 45개 초과 시 4분할 재귀
        if search_count > 45:
            print('⚠️ big data dividing...')
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2
            resp_list.extend(get_store_list(start_x, start_y, dividing_x, dividing_y))
            resp_list.extend(get_store_list(dividing_x, start_y, end_x, dividing_y))
            resp_list.extend(get_store_list(start_x, dividing_y, dividing_x, end_y))
            resp_list.extend(get_store_list(dividing_x, dividing_y, end_x, end_y))
            break

        # 🔸 데이터 추가
        resp_list.extend(data['documents'])

        # 더 이상 페이지 없으면 종료
        if data['meta'].get('is_end', True):
            break

        cnt += 1
        time.sleep(0.1)  # rate limit 완화

    return resp_list



# 용두동 좌표 (스퀘어좌표)
start_x, start_y = 127.02, 37.57
end_x, end_y = 127.04, 37.59

# 격자 크기
jump_x = 0.02
jump_y = 0.02

# 최종 데이터가 담길 리스트
CS2_list = []

# X축 반복
x = start_x_min
while x < end_x_max:
    rect_end_x = min(x + jump_x, end_x_max)

    # Y축 반복
    y = start_y_min
    while y < end_y_max:
        rect_end_y = min(y + jump_y, end_y_max)

        # POI 수집
        CS2_list_one = get_store_list(x, y, rect_end_x, rect_end_y)
        CS2_list.extend(CS2_list_one)

        # Y 증가
        y = rect_end_y
    # X 증가
    x = rect_end_x

print(f"총 POI 수집 건수: {len(CS2_list)}")