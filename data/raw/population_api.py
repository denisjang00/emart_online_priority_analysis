import requests
import os

from dotenv import load_dotenv
from data.raw.cache_utils import load_cache, save_cache

load_dotenv()

API_KEY = os.getenv("PUBLIC_DATA_API_KEY")

CACHE_PATH = "data/cache/population_cache.csv"

def get_population(roadNmCd, year=202401):
    url = "http://apis.data.go.kr/1741000/rnPpltnHhStus/selectRnPpltnHhStus"

    params = {
        "serviceKey": API_KEY,
        "roadNmCd": roadNmCd,
        "srchFrYm": year,
        "srchToYm": year,
        "type": "JSON",
        "numOfRows": 100,
        "pageNo": 1
    }

    res = requests.get(url, params=params)
    data = res.json()

    try:
        items = data["Response"]["items"]["item"]
        pop = sum(int(i["totNmprCnt"]) for i in items)
        hh = sum(int(i["hhCnt"]) for i in items)
        return pop, hh
    except:
        return 0, 0

def add_population(df):

    cache = load_cache(CACHE_PATH, "roadNmCd")

    pops, hhs = [], []

    for code in df["roadNmCd"]:

        key = str(code)

        if key in cache:
            pops.append(cache[key]["population"])
            hhs.append(cache[key]["household"])

        else:
            p, h = get_population(int(code))

            cache[key] = {
                "population": p,
                "household": h
            }

            pops.append(p)
            hhs.append(h)

    save_cache(cache, CACHE_PATH, "roadNmCd")

    df["population23"] = pops
    df["household23"] = hhs

    return df