import urllib
import json
import os

from dotenv import load_dotenv
from data.raw.cache_utils import load_cache, save_cache

load_dotenv()

VWORLD_API_KEY = os.getenv("VWORLD_API_KEY")

CACHE_PATH = "data/cache/geocode_cache.csv"

def get_geocode(addr, mode="ROAD"):
    q = urllib.parse.quote(addr)
    url = f"http://api.vworld.kr/req/address?service=address&type={mode}&request=getCoord&key={VWORLD_API_KEY}&address={q}"

    try:
        data = urllib.request.urlopen(url)
    except Exception as e:
        print(f"[ERROR] Geocode 실패: {e}")
        return 0, 0
    
    result = json.loads(data.read())

    if result['response']['status'] == 'OK':
        x = float(result['response']['result']['point']['x'])
        y = float(result['response']['result']['point']['y'])
        return x, y

    return 0, 0

def add_coordinates(df):

    cache = load_cache(CACHE_PATH, "address")

    x_vals, y_vals = [], []

    for road, local in zip(df["road_address"], df["local_address"]):

        key = road

        # 캐시 우선 사용
        if key in cache:
            x = cache[key]["longitude"]
            y = cache[key]["latitude"]

        else:
            x, y = get_geocode(road, "ROAD")

            if x == 0:
                x, y = get_geocode(local, "PARCEL")

            # 캐시에 저장
            cache[key] = {
                "longitude": x,
                "latitude": y
            }

        x_vals.append(x)
        y_vals.append(y)

    save_cache(cache, CACHE_PATH, "address")

    df["longitude"] = x_vals
    df["latitude"] = y_vals

    return df