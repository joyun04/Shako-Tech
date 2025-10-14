
#특정 poi를 긁어오기위해 kakao map을 활용했습니다
# https://apis.map.kakao.com/
# * 트래킹 제한: 1일 300,000회 사용가능합니다


import requests
import folium
import collections
from tinydb import TinyDB,Query
import pandas as pd

# 잘작동 되는지 확인용 (Test)
# kakao api 사용하기 위한 key
app_key = 'KakaoAK' + 'f7dea420445453a99101987bcf736ac3'
url = 'https://dapi.kakao.com/v2/local/search/category.json'
params = {
    'category_group_code' : 'FD6',
    'page': 1,
    'rect': '127.0085280000,37.5357715389,127.1221115536,37.4573204481',
}
headers  = {
    'Authorization': 'KakaoAK f7dea420445453a99101987bcf736ac3'
}
resp = requests.get(url, params=params, headers=headers)
# 바이트 → 문자열 → JSON
# resp.json()을 쓰면 내부적으로 utf-8로 디코딩해서 dict로 반환
data = resp.json()
# 카카오 로컬 API 기준: 'documents' key에 장소 정보 리스트
documents = data['documents']

# 4️⃣ DataFrame으로 변환
df = pd.DataFrame(documents)

print(df.head())