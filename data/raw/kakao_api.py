import requests
import os
import pandas as pd

from dotenv import load_dotenv

from data.raw.cache_utils import load_cache, save_cache

load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

HEADERS = {
    "Authorization": f"KakaoAK {KAKAO_API_KEY}"
}

CACHE_PATH = "data/cache/kakao_cache.csv"

def get_nearby_count(x, y, keyword, radius=1000):
    """
    좌표 기준으로 특정 키워드(대형마트 등) 개수 조회
    """

    # 좌표 이상 방지 (0, None 등)
    if x == 0 or y == 0:
        return 0

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    total_count = 0
    page = 1

    while True:
        params = {
            "query": keyword,
            "x": x,
            "y": y,
            "radius": radius,
            "page": page,
            "size": 15
        }

        try:
            res = requests.get(url, headers=HEADERS, params=params, timeout=5)

            if res.status_code != 200:
                print(f"[ERROR] Kakao API 상태코드: {res.status_code}")
                return 0

            data = res.json()

        except Exception as e:
            print(f"[ERROR] Kakao API 호출 실패: {e}")
            return 0

        docs = data.get("documents", [])
        total_count += len(docs)

        if data.get("meta", {}).get("is_end", True):
            break

        page += 1

    return total_count

def add_competition(df):
    """
    점포별 경쟁 점포 수 추가 (캐싱 적용)
    """

    # 캐시 로드
    cache = load_cache(CACHE_PATH, "key")

    competitor_list = []
    density_list = []

    for _, row in df.iterrows():

        x, y = row["longitude"], row["latitude"]

        # 캐시 키 (좌표 기준)
        key = f"{round(x, 5)}_{round(y, 5)}"

        # 캐시 사용
        if key in cache:
            comp = cache[key]["competitor"]
            dens = cache[key]["density"]

        else:
            # 1. 경쟁 점포 (대형마트)
            comp = get_nearby_count(
                x, y,
                keyword="대형마트",
                radius=1000
            )

            # 2. 상권 밀도 (마트 전체)
            dens = get_nearby_count(
                x, y,
                keyword="마트",
                radius=500
            )

            # 캐시 저장 조건
            if comp == 0 and dens == 0:
                print(f"[WARN] 0 결과 → 캐시 저장 스킵: {row['store_name']}")
            else:
                cache[key] = {
                    "competitor": comp,
                    "density": dens
                }

        competitor_list.append(comp)
        density_list.append(dens)

    save_cache(cache, CACHE_PATH, "key")

    df["competitor_count"] = competitor_list
    df["market_density"] = density_list

    return df